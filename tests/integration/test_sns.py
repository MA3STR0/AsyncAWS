import os
from asyncaws import SNS
from tornado.testing import AsyncTestCase, gen_test
from random import randint

aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_key_secret = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_REGION']


class TestSQS(AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        cls.sns = SNS(aws_key_id, aws_key_secret, aws_region, async=False)
        cls.topic_name = "test-topic-%s" % randint(1000, 9999)
        cls.topic_arn = cls.sns.create_topic(cls.topic_name)

    @classmethod
    def tearDownClass(cls):
        cls.sns.delete_topic(cls.topic_arn)

    @gen_test
    def test_topic_actions(self):
        self.assertTrue(self.topic_arn.startswith('arn:'))
