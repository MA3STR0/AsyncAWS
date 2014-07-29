import os
import sys
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from asyncaws import SQS

ioloop = IOLoop.current()
aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_key_secret = os.environ['AWS_SECRET_ACCESS_KEY']

sqs = SQS(aws_key_id, aws_key_secret, "eu-west-1")

@coroutine
def create_and_send():
    """Create an SQS queue and send a message"""
    queue_url = yield sqs.create_queue("test-queue")
    yield sqs.send_message(queue_url, "Hello, World!")
    sys.exit(0)


if __name__ == '__main__':
    ioloop.add_callback(create_and_send)
    ioloop.start()