SNS: Async Python API
=====================

About
-----
Amazon Simple Notification Service (SNS) is a web service that helps building distributed applications.
It can broadcast real-time notification messages to interested subscribers over multiple delivery protocols,
it particular Amazon SQS.

AWS documentation: http://docs.aws.amazon.com/sns/latest/api/Welcome.html

This module implements fully asynchronous access to SNS API in Python.

Examples
--------
Don't forget to set your AWS keys before running examples. You can set environment variables in your .profile, or just run
::

    AWS_ACCESS_KEY_ID=id AWS_SECRET_ACCESS_KEY=secret python example.py

**Example 1.** Create a queue and send "Hello, World!" message to it.

.. literalinclude:: /../examples/sqs/create_and_send.py

**Example 2.** Listen to the queue and trigger `on_message` callback

.. literalinclude:: /../examples/sqs/on_message_callback.py

API documentation
-----------------

.. autoclass:: asyncaws.SNS
    :members:

.. _CreateTopic: http://docs.aws.amazon.com/sns/latest/APIReference/API_CreateTopic.html
.. _Subscribe:  http://docs.aws.amazon.com/sns/latest/APIReference/API_Subscribe.html
.. _ConfirmSubscription: http://docs.aws.amazon.com/sns/latest/APIReference/API_ConfirmSubscription.html
.. _Publish: http://docs.aws.amazon.com/sns/latest/APIReference/API_ConfirmSubscription.html

