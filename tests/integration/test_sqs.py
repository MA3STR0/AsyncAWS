import os
from asyncaws import SQS
from tornado.testing import AsyncTestCase, gen_test
from random import randint

aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_key_secret = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_REGION']
aws_test_account_id = "637085312181"


class TestSQS(AsyncTestCase):

    @classmethod
    def setUpClass(cls):
        cls.sqs = SQS(aws_key_id, aws_key_secret, aws_region, async=False)
        cls.queue_name = "test-queue-%s" % randint(1000, 9999)
        cls.queue_url = cls.sqs.create_queue(
            cls.queue_name, {"MessageRetentionPeriod": 60})

    @classmethod
    def tearDownClass(cls):
        cls.sqs.delete_queue(cls.queue_url)

    @gen_test
    def test_queue_actions(self):
        self.assertTrue(self.queue_url.startswith('http'))
        get_attr_result = self.sqs.get_queue_attributes(
            self.queue_url, ['MessageRetentionPeriod'])
        self.assertIsInstance(get_attr_result, dict)
        self.assertEqual(get_attr_result['MessageRetentionPeriod'], '60')
        add_perm_result = self.sqs.add_permission(
            self.queue_url, [aws_test_account_id], ["SendMessage"], "test-permission-id")
        self.assertIsInstance(add_perm_result, str)
