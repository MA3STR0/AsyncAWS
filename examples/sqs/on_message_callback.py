import os
from functools import partial
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from asyncaws import SQS

ioloop = IOLoop.current()
aws_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_key_secret = os.environ['AWS_SECRET_ACCESS_KEY']

sqs = SQS(aws_key_id, aws_key_secret, "eu-west-1")
queue_url = "https://sqs.eu-west-1.amazonaws.com/637085312181/test-queue"

@coroutine
def listen_queue():
    """Wait for SQS messages using async long polling"""
    # tornado will "pause" the coroutine here until SQS returns something
    message = yield sqs.listen_queue(queue_url)
    if message:
        # schedule the callback
        ioloop.add_callback(partial(on_message, message))
    # reconnect to SQS and repeat everything
    ioloop.add_callback(listen_queue)


@coroutine
def on_message(message):
    """This function will be called when new message arrives"""
    print "New message received:", message['Body']
    yield sqs.delete_message(queue_url, message['ReceiptHandle'])


if __name__ == '__main__':
    ioloop.add_callback(listen_queue)
    ioloop.start()