import os
import sys
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from asyncaws import SNS

ioloop = IOLoop.current()
aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_key_secret = os.environ['AWS_SECRET_ACCESS_KEY']

sns = SNS(aws_key_id, aws_key_secret, "eu-west-1")


@coroutine
def create_and_publish():
    """Create an SQS queue and send a message"""
    topic_arn = yield sns.create_topic("test-topic")
    yield sns.publish("Hello, World!", "Some subject", topic_arn)
    sys.exit(0)


if __name__ == '__main__':
    ioloop.add_callback(create_and_publish)
    ioloop.start()