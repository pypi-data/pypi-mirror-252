from unittest import TestCase

from cloudshell.cp.aws.common import retry_helper


class TestRetryHelper(TestCase):
    counter = 0

    def setUp(self):
        TestRetryHelper.counter = 0

    def test_retry_action_executed_3_times(self):
        def test_method():
            TestRetryHelper.counter += 1
            if TestRetryHelper.counter != 3:
                raise Exception()

        retry_helper.do_with_retry(test_method)

        assert TestRetryHelper.counter == 3
