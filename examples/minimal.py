from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from asyncaws import SQS

sqs = SQS('aws-key-id', 'sqs-key-secret', 'eu-west-1')
ioloop = IOLoop.current()

@coroutine
def main():
    queue_url = yield sqs.create_queue("test-queue")
    message_id = yield sqs.send_message(queue_url, "Hello, World!")
    print queue_url, message_id

if __name__ == '__main__':
    ioloop.add_callback(main)
    ioloop.start()
