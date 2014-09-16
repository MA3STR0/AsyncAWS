import os
from asyncaws import SQS
from tornado.testing import AsyncTestCase, gen_test

aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_key_secret = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_REGION']


class TestSQS(AsyncTestCase):
    sqs = SQS(aws_key_id, aws_key_secret, aws_region, async=False)

    @gen_test(timeout=60)
    def test_create_queue(self):
        queue_url = self.sqs.create_queue(
            "test-queue", {"MessageRetentionPeriod": 60})
        self.assertIsInstance(queue_url, str)
        self.assertTrue(queue_url.startswith('http'))
        get_attr_result = self.sqs.get_queue_attributes(
            queue_url, ['MessageRetentionPeriod'])
        self.assertIsInstance(get_attr_result, dict)
        self.assertEqual(get_attr_result['MessageRetentionPeriod'], '60')
        add_perm_result = self.sqs.add_permission(
            queue_url, ['637085312181'], ["SendMessage"], "test-permission-id")
        self.assertIsInstance(add_perm_result, str)
        delete_result = self.sqs.delete_queue(queue_url)
        self.assertIsInstance(delete_result, str)
