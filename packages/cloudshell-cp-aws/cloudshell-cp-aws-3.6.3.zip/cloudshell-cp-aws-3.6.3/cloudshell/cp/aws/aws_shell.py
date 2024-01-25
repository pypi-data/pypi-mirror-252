from __future__ import annotations

import json

import jsonpickle
from botocore.exceptions import ClientError, NoCredentialsError

from cloudshell.cp.core.drive_request_parser import DriverRequestParser
from cloudshell.cp.core.models import ConnectSubnet, DeployApp, VmDetailsData
from cloudshell.cp.core.utils import single

from cloudshell.cp.aws.common.deploy_data_holder import DeployDataHolder
from cloudshell.cp.aws.domain.ami_management.operations.access_key_operation import (
    GetAccessKeyOperation,
)
from cloudshell.cp.aws.domain.ami_management.operations.delete_operation import (
    DeleteAMIOperation,
)
from cloudshell.cp.aws.domain.ami_management.operations.deploy_operation import (
    DeployAMIOperation,
)
from cloudshell.cp.aws.domain.ami_management.operations.power_operation import (
    PowerOperation,
)
from cloudshell.cp.aws.domain.ami_management.operations.refresh_ip_operation import (
    RefreshIpOperation,
)
from cloudshell.cp.aws.domain.ami_management.operations.snapshot_operation import (
    SnapshotOperation,
)
from cloudshell.cp.aws.domain.common.cancellation_service import (
    CommandCancellationService,
)
from cloudshell.cp.aws.domain.common.vm_details_provider import VmDetailsProvider
from cloudshell.cp.aws.domain.conncetivity.operations.cleanup import (
    CleanupSandboxInfraOperation,
)
from cloudshell.cp.aws.domain.conncetivity.operations.prepare import (
    PrepareSandboxInfraOperation,
)
from cloudshell.cp.aws.domain.conncetivity.operations.traffic_mirroring_operation import (  # noqa
    TrafficMirrorOperation,
)
from cloudshell.cp.aws.domain.context.aws_shell import AwsShellContext
from cloudshell.cp.aws.domain.deployed_app.operations.app_ports_operation import (
    DeployedAppPortsOperation,
)
from cloudshell.cp.aws.domain.deployed_app.operations.set_app_security_groups import (
    SetAppSecurityGroupsOperation,
)
from cloudshell.cp.aws.domain.deployed_app.operations.vm_details_operation import (
    VmDetailsOperation,
)
from cloudshell.cp.aws.domain.handlers.ec2 import TagsHandler
from cloudshell.cp.aws.domain.operations.autoload_operation import AutoloadOperation
from cloudshell.cp.aws.domain.services.cloudshell.cs_subnet_service import (
    CsSubnetService,
)
from cloudshell.cp.aws.domain.services.cloudshell.traffic_mirror_pool_services import (
    SessionNumberService,
)
from cloudshell.cp.aws.domain.services.ec2.ebs import EC2StorageService
from cloudshell.cp.aws.domain.services.ec2.elastic_ip import ElasticIpService
from cloudshell.cp.aws.domain.services.ec2.instance import InstanceService
from cloudshell.cp.aws.domain.services.ec2.instance_credentials import (
    InstanceCredentialsService,
)
from cloudshell.cp.aws.domain.services.ec2.keypair import KeyPairService
from cloudshell.cp.aws.domain.services.ec2.mirroring import TrafficMirrorService
from cloudshell.cp.aws.domain.services.ec2.network_interface import (
    NetworkInterfaceService,
)
from cloudshell.cp.aws.domain.services.ec2.security_group import SecurityGroupService
from cloudshell.cp.aws.domain.services.ec2.subnet import SubnetService
from cloudshell.cp.aws.domain.services.ec2.vpc import VPCService
from cloudshell.cp.aws.domain.services.parsers.aws_model_parser import AWSModelsParser
from cloudshell.cp.aws.domain.services.parsers.command_results_parser import (
    CommandResultsParser,
)
from cloudshell.cp.aws.domain.services.parsers.custom_param_extractor import (
    VmCustomParamsExtractor,
)
from cloudshell.cp.aws.domain.services.s3.bucket import S3BucketService
from cloudshell.cp.aws.domain.services.session_providers.aws_session_provider import (
    AWSSessionProvider,
)
from cloudshell.cp.aws.domain.services.strategy.device_index import (
    AllocateMissingValuesDeviceIndexStrategy,
)
from cloudshell.cp.aws.domain.services.waiters.ami import AMIWaiter
from cloudshell.cp.aws.domain.services.waiters.instance import InstanceWaiter
from cloudshell.cp.aws.domain.services.waiters.password import PasswordWaiter
from cloudshell.cp.aws.domain.services.waiters.subnet import SubnetWaiter
from cloudshell.cp.aws.domain.services.waiters.vpc import VPCWaiter
from cloudshell.cp.aws.models.network_actions_models import (
    SetAppSecurityGroupActionResult,
)
from cloudshell.cp.aws.models.reservation_model import ReservationModel
from cloudshell.cp.aws.models.vm_details import VmDetailsRequest


class AWSShell:
    CREDENTIALS_ERROR_MESSAGE = (
        "Oops, looks like there was a problem with "
        "your cloud provider credentials. "
        "Please check AWS Secret Access Key "
        "and AWS Access Key ID"
    )

    def __init__(self):
        self.image_waiter = AMIWaiter()
        self.command_result_parser = CommandResultsParser()
        self.cancellation_service = CommandCancellationService()
        self.ec2_instance_waiter = InstanceWaiter(
            cancellation_service=self.cancellation_service
        )
        self.ec2_storage_service = EC2StorageService()
        self.model_parser = AWSModelsParser()
        self.aws_session_manager = AWSSessionProvider()
        self.password_waiter = PasswordWaiter(self.cancellation_service)
        self.vm_custom_params_extractor = VmCustomParamsExtractor()
        self.ami_credentials_service = InstanceCredentialsService(self.password_waiter)
        self.security_group_service = SecurityGroupService()
        self.subnet_waiter = SubnetWaiter()
        self.subnet_service = SubnetService(self.subnet_waiter)
        self.s3_service = S3BucketService()
        self.key_pair_service = KeyPairService(self.s3_service)
        self.vpc_waiter = VPCWaiter()
        self.network_interface_service = NetworkInterfaceService(
            subnet_service=self.subnet_service,
            security_group_service=self.security_group_service,
        )
        self.instance_service = InstanceService(
            self.ec2_instance_waiter, self.network_interface_service
        )
        self.elastic_ip_service = ElasticIpService()
        self.vm_details_provider = VmDetailsProvider()
        self.session_number_service = SessionNumberService()
        self.traffic_mirror_service = TrafficMirrorService()
        self.request_parser = DriverRequestParser()

        self.vpc_service = VPCService(
            subnet_service=self.subnet_service,
            instance_service=self.instance_service,
            vpc_waiter=self.vpc_waiter,
            sg_service=self.security_group_service,
            traffic_mirror_service=self.traffic_mirror_service,
        )
        self.prepare_connectivity_operation = PrepareSandboxInfraOperation(
            vpc_service=self.vpc_service,
            security_group_service=self.security_group_service,
            key_pair_service=self.key_pair_service,
            subnet_service=self.subnet_service,
            subnet_waiter=self.subnet_waiter,
        )

        self.deploy_ami_operation = DeployAMIOperation(
            instance_service=self.instance_service,
            ami_credential_service=self.ami_credentials_service,
            security_group_service=self.security_group_service,
            vpc_service=self.vpc_service,
            key_pair_service=self.key_pair_service,
            subnet_service=self.subnet_service,
            elastic_ip_service=self.elastic_ip_service,
            network_interface_service=self.network_interface_service,
            device_index_strategy=AllocateMissingValuesDeviceIndexStrategy(),
            vm_details_provider=self.vm_details_provider,
        )

        self.refresh_ip_operation = RefreshIpOperation(
            instance_service=self.instance_service
        )

        self.power_management_operation = PowerOperation(
            instance_service=self.instance_service,
            instance_waiter=self.ec2_instance_waiter,
        )

        self.delete_ami_operation = DeleteAMIOperation(
            instance_service=self.instance_service,
            ec2_storage_service=self.ec2_storage_service,
            security_group_service=self.security_group_service,
            elastic_ip_service=self.elastic_ip_service,
        )

        self.clean_up_operation = CleanupSandboxInfraOperation(
            vpc_service=self.vpc_service,
            key_pair_service=self.key_pair_service,
        )

        self.deployed_app_ports_operation = DeployedAppPortsOperation(
            self.vm_custom_params_extractor,
            security_group_service=self.security_group_service,
            instance_service=self.instance_service,
        )

        self.access_key_operation = GetAccessKeyOperation(
            key_pair_service=self.key_pair_service
        )

        self.set_app_security_groups_operation = SetAppSecurityGroupsOperation(
            instance_service=self.instance_service,
            security_group_service=self.security_group_service,
        )

        self.vm_details_operation = VmDetailsOperation(
            instance_service=self.instance_service,
            vm_details_provider=self.vm_details_provider,
        )

        self.autoload_operation = AutoloadOperation()

        self.snapshot_operation = SnapshotOperation(
            self.instance_service, self.image_waiter
        )

        self.traffic_mirroring_operation = TrafficMirrorOperation(
            session_number_service=self.session_number_service,
            traffic_mirror_service=self.traffic_mirror_service,
            cancellation_service=self.cancellation_service,
        )

    def cleanup_connectivity(self, command_context, actions):
        """Will delete the reservation vpc and all related resources."""
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Cleanup Connectivity")

            result = self.clean_up_operation.cleanup(
                shell_context.aws_api,
                shell_context.aws_ec2_resource_model,
                command_context.reservation.reservation_id,
                actions,
                shell_context.logger,
            )
            return self.command_result_parser.set_command_result(
                {"driverResponse": {"actionResults": [result]}}
            )

    def prepare_connectivity(self, command_context, actions, cancellation_context):
        """# noqa
        Will create a vpc for the reservation and will peer it with the management vpc
        :param ResourceCommandContext command_context: The Command Context
        :param list[RequestActionBase] actions:
        :return: json string response
        :param CancellationContext cancellation_context:
        :rtype: list[ActionResultBase]
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Prepare Connectivity")
            reservation = self.model_parser.convert_to_reservation_model(
                command_context.reservation
            )
            cs_subnet_service = CsSubnetService(
                shell_context.cloudshell_session, reservation.reservation_id
            )

            results = self.prepare_connectivity_operation.prepare_connectivity(
                aws_clients=shell_context.aws_api,
                reservation=reservation,
                aws_model=shell_context.aws_ec2_resource_model,
                actions=actions,
                cancellation_context=cancellation_context,
                cs_subnet_service=cs_subnet_service,
                logger=shell_context.logger,
            )
            return results

    def get_inventory(self, command_context):
        """Validate Cloud Provider.

        :param command_context: ResourceCommandContext
        """
        try:
            with AwsShellContext(
                context=command_context, aws_session_manager=self.aws_session_manager
            ) as shell_context:
                shell_context.logger.info("Starting Autoload Operation...")
                result = self.autoload_operation.get_inventory(
                    cloud_provider_model=shell_context.aws_ec2_resource_model,
                    logger=shell_context.logger,
                    ec2_client=shell_context.aws_api.ec2_client,
                    ec2_session=shell_context.aws_api.ec2_session,
                    s3_session=shell_context.aws_api.s3_session,
                )
                shell_context.logger.info("End Autoload Operation...")
                return result

        except ClientError as ce:
            if "AuthorizationHeaderMalformed" in str(ce):
                raise Exception(self.CREDENTIALS_ERROR_MESSAGE)
            raise ce

        except NoCredentialsError:
            raise Exception(self.CREDENTIALS_ERROR_MESSAGE)

        except ValueError as ve:
            if "Invalid endpoint" in str(ve):
                raise Exception(
                    "Oops, like you didnt configure Region correctly. Please select "
                    "Region and try again "
                )
            else:
                raise ve

    def power_on_ami(self, command_context):
        """# noqa
        Will power on the ami
        :param ResourceRemoteCommandContext command_context:
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Power On")

            resource = command_context.remote_endpoints[0]
            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )

            self.power_management_operation.power_on(
                ec2_session=shell_context.aws_api.ec2_session,
                ami_id=data_holder.vmdetails.uid,
            )

    def power_off_ami(self, command_context):
        """# noqa
        Will power on the ami
        :param ResourceRemoteCommandContext command_context:
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Power Off")

            resource = command_context.remote_endpoints[0]
            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )

            self.power_management_operation.power_off(
                ec2_session=shell_context.aws_api.ec2_session,
                ami_id=data_holder.vmdetails.uid,
            )

    def delete_instance(self, command_context):
        """# noqa
        Will delete the ami instance
        :param ResourceRemoteCommandContext command_context:
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Delete instance")

            resource = command_context.remote_endpoints[0]
            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )

            self.delete_ami_operation.delete_instance(
                logger=shell_context.logger,
                ec2_session=shell_context.aws_api.ec2_session,
                iam_client=shell_context.aws_api.iam_client,
                instance_id=data_holder.vmdetails.uid,
                vm_name=data_holder.name,
                reservation=self.model_parser.convert_to_reservation_model(
                    command_context.remote_reservation,
                ),
            )

    def get_application_ports(self, command_context):
        """# noqa
        Will return the application ports in a nicely formated manner
        :param ResourceRemoteCommandContext command_context:
        :rtype: str
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Get Application Ports")
            resource = command_context.remote_endpoints[0]

            # Get instance id
            deployed_instance_id = (
                self.model_parser.try_get_deployed_connected_resource_instance_id(
                    command_context
                )
            )

            # Get Allow all Storage Traffic on deployed resource
            allow_all_storage_traffic = self.model_parser.get_allow_all_storage_traffic_from_connected_resource_details(  # noqa
                command_context
            )

            return self.deployed_app_ports_operation.get_app_ports_from_cloud_provider(
                ec2_session=shell_context.aws_api.ec2_session,
                instance_id=deployed_instance_id,
                resource=resource,
                allow_all_storage_traffic=allow_all_storage_traffic,
            )

    def deploy_ami(self, command_context, actions, cancellation_context):
        """# noqa
        Will deploy Amazon Image on the cloud provider
        :param ResourceCommandContext command_context:
        :param list[RequestActionBase] actions::
        :param CancellationContext cancellation_context:
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Deploying AMI")

            deploy_action = single(actions, lambda x: isinstance(x, DeployApp))
            network_actions = [a for a in actions if isinstance(a, ConnectSubnet)]

            deploy_data = self.deploy_ami_operation.deploy(
                ec2_session=shell_context.aws_api.ec2_session,
                s3_session=shell_context.aws_api.s3_session,
                iam_client=shell_context.aws_api.iam_client,
                name=deploy_action.actionParams.appName,
                reservation=self.model_parser.convert_to_reservation_model(
                    command_context.reservation
                ),
                aws_ec2_cp_resource_model=shell_context.aws_ec2_resource_model,
                ami_deploy_action=deploy_action,
                network_actions=network_actions,
                ec2_client=shell_context.aws_api.ec2_client,
                cancellation_context=cancellation_context,
                logger=shell_context.logger,
            )

            return deploy_data

    def refresh_ip(self, command_context):
        """# noqa
        :param ResourceRemoteCommandContext command_context:
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Refresh IP")

            # Get Private Ip on deployed resource
            private_ip_on_resource = (
                self.model_parser.get_private_ip_from_connected_resource_details(
                    command_context
                )
            )
            # Get Public IP on deployed resource

            (
                public_ip_attr_name,
                public_ip_on_resource,
            ) = self.model_parser.get_public_ip_attr_from_connected_resource_details(
                command_context
            )
            # Get instance id
            deployed_instance_id = (
                self.model_parser.try_get_deployed_connected_resource_instance_id(
                    command_context
                )
            )
            # Get connected resource name
            resource_fullname = self.model_parser.get_connectd_resource_fullname(
                command_context
            )

            self.refresh_ip_operation.refresh_ip(
                cloudshell_session=shell_context.cloudshell_session,
                ec2_session=shell_context.aws_api.ec2_session,
                deployed_instance_id=deployed_instance_id,
                private_ip_on_resource=private_ip_on_resource,
                public_ip_on_resource=public_ip_on_resource,
                public_ip_attribute_name=public_ip_attr_name,
                resource_fullname=resource_fullname,
            )

    def get_access_key(self, command_context):
        """# noqa
        Returns the pem file for the connected resource
        :param ResourceRemoteCommandContext command_context:
        :rtype str:
        """
        with AwsShellContext(
            context=command_context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("GetAccessKey")
            reservation_id = self._get_reservation_id(command_context)
            return self.access_key_operation.get_access_key(
                s3_session=shell_context.aws_api.s3_session,
                aws_ec2_resource_model=shell_context.aws_ec2_resource_model,
                reservation_id=reservation_id,
            )

    def set_app_security_groups(self, context, request):
        """# noqa
        Set security groups (inbound rules only)
        :param context: todo - set the type of the parameter
        :param request: The json request
        :return:
        """
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Set App Security Groups")

            reservation = self.model_parser.convert_to_reservation_model(
                context.reservation
            )
            app_security_group_models = (
                self.model_parser.convert_to_app_security_group_models(request)
            )

            result = self.set_app_security_groups_operation.set_apps_security_groups(
                app_security_group_models=app_security_group_models,
                reservation=reservation,
                ec2_session=shell_context.aws_api.ec2_session,
                logger=shell_context.logger,
            )

            json_result = SetAppSecurityGroupActionResult.to_json(result)

            return json_result

    def get_vm_details(self, context, cancellation_context, requests_json):
        """# noqa
        Get vm details for specific deployed app
        :type context: ResourceCommandContext
        :rtype str
        """
        results = []
        vm_details_requests = [
            VmDetailsRequest(item)
            for item in DeployDataHolder(jsonpickle.decode(requests_json)).items
        ]

        for request in vm_details_requests:
            if cancellation_context.is_cancelled:
                break

            try:
                with AwsShellContext(
                    context=context, aws_session_manager=self.aws_session_manager
                ) as shell_context:
                    shell_context.logger.info("Get VmDetails")
                    vm_details = self.vm_details_operation.get_vm_details(
                        request.uuid, shell_context.aws_api.ec2_session
                    )
                    vm_details.appName = request.app_name
                    results.append(vm_details)
            except Exception as e:
                result = VmDetailsData()
                result.appName = request.app_name
                result.error = str(e)
                results.append(result)

        return self.command_result_parser.set_command_result(results)

    def remote_get_snapshots(self, context):
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Get Snapshots")

            resource = context.remote_endpoints[0]
            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )

            return self.snapshot_operation.get_snapshots(
                shell_context.aws_api.ec2_client, instance_id=data_holder.vmdetails.uid
            )

    def remote_save_snapshot(self, context, snapshot_name):
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Save Snapshot")
            resource = context.remote_endpoints[0]
            reservation = ReservationModel(context.remote_reservation)
            tags = TagsHandler.create_default_tags(snapshot_name, reservation)
            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )
            self.snapshot_operation.save_snapshot(
                ec2_client=shell_context.aws_api.ec2_client,
                ec2_session=shell_context.aws_api.ec2_session,
                instance_id=data_holder.vmdetails.uid,
                snapshot_name=snapshot_name,
                tags=tags.aws_tags,
            )

    def remote_restore_snapshot(self, context, snapshot_name):
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Save Snapshot")
            resource = context.remote_endpoints[0]
            reservation = ReservationModel(context.remote_reservation)
            tags = TagsHandler.create_default_tags(snapshot_name, reservation)
            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )
            self.snapshot_operation.save_snapshot(
                ec2_client=shell_context.aws_api.ec2_client,
                ec2_session=shell_context.aws_api.ec2_session,
                instance_id=data_holder.vmdetails.uid,
                snapshot_name=snapshot_name,
                tags=tags.aws_tags,
            )

    def save_app(self, context, cancellation_context):
        """# noqa
        :param context:
        :param cancellation_context:
        :return:
        """
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Save Snapshot")

            resource = context.remote_endpoints[0]

            data_holder = self.model_parser.convert_app_resource_to_deployed_app(
                resource
            )
            resource_fullname = self.model_parser.get_connectd_resource_fullname(
                context
            )

            image_id = self.snapshot_operation.save(
                logger=shell_context.logger,
                ec2_session=shell_context.aws_api.ec2_session,
                instance_id=data_holder.vmdetails.uid,
                deployed_app_name=resource_fullname,
                snapshot_prefix="",
                no_reboot=True,
            )

            return json.dumps({"AWS EC2 Instance.AWS AMI Id": image_id})

    def add_custom_tags(self, context, request):
        """# noqa
        :param ResourceCommandContext context:
        :param str request:
        :return:
        """
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Add custom tags")

            # Get instance id
            deployed_instance_id = (
                self.model_parser.try_get_deployed_connected_resource_instance_id(
                    context
                )
            )

            tags = TagsHandler.from_tags_list(json.loads(request))

            instance = self.instance_service.get_instance_by_id(
                shell_context.aws_api.ec2_session, deployed_instance_id
            )
            tags.add_tags_to_obj(instance)

    def create_traffic_mirroring(self, context, cancellation_context, request):
        """# noqa
        Will create a vpc for the reservation and will peer it with the management vpc
        :param request:
        :param ResourceCommandContext context:

        :return: json string response
        :param CancellationContext cancellation_context:
        :rtype: list[ActionResultBase]
        """
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Create traffic mirroring")
            actions = self._parse_request(request, shell_context)
            self.traffic_mirroring_operation.validate_create_actions(
                actions, request, shell_context.logger
            )
            results = self.traffic_mirroring_operation.create(
                ec2_client=shell_context.aws_api.ec2_client,
                reservation=self.model_parser.convert_to_reservation_model(
                    context.reservation
                ),
                actions=actions,
                cancellation_context=cancellation_context,
                logger=shell_context.logger,
                cloudshell=shell_context.cloudshell_session,
            )

            return results

    def _parse_request(self, request, shell_context):
        try:
            actions = self.request_parser.convert_driver_request_to_actions(request)
            if not actions:
                raise Exception("Invalid request: " + request)
        except Exception as e:
            shell_context.logger.exception("Invalid request " + request)
            raise e
        return actions

    @staticmethod
    def _get_reservation_id(context):
        reservation_id = None
        reservation = getattr(
            context, "reservation", getattr(context, "remote_reservation", None)
        )
        if reservation:
            reservation_id = reservation.reservation_id
        return reservation_id

    def remove_traffic_mirroring(self, context, request):
        """# noqa
        Can remove traffic mirroring sessions by session id, or all sessions associated with a traffic mirror target (by target nic id)
        :param str request:
        :param ResourceCommandContext context:
        :param ResourceCommandContext context:

        :return: json string response
        :rtype: list[ActionResultBase]
        """
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Create traffic mirroring")

            self.traffic_mirroring_operation.validate_remove_request(
                request, shell_context.logger
            )

            actions = self._parse_request(request, shell_context)

            results = self.traffic_mirroring_operation.remove(
                ec2_client=shell_context.aws_api.ec2_client,
                reservation=self.model_parser.convert_to_reservation_model(
                    context.reservation
                ),
                actions=actions,
                logger=shell_context.logger,
                cloudshell=shell_context.cloudshell_session,
            )

            return results

    def assign_additional_private_ipv4s(self, context, vnic_id, new_ips):
        with AwsShellContext(
            context=context, aws_session_manager=self.aws_session_manager
        ) as shell_context:
            shell_context.logger.info("Assign additional IP Addresses")

            ips = list(map(str.strip, new_ips.split(";")))
            try:
                response = shell_context.aws_api.ec2_client.assign_private_ip_addresses(
                    AllowReassignment=True,
                    NetworkInterfaceId=vnic_id,
                    PrivateIpAddresses=ips,
                )
                assigned_ips_response = response.get("AssignedPrivateIpAddresses", [])
                return ";".join(
                    [
                        ip.get("PrivateIpAddress")
                        for ip in assigned_ips_response
                        if ip.get("PrivateIpAddress")
                    ]
                )
            except Exception:
                shell_context.logger.error("Failed to add ips", exc_info=True)
                return None
