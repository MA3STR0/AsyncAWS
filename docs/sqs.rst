SQS: Async Python API
=====================

About
-----
Amazon Simple Queue Service (SQS) is a hosted messaging queue service that handles text data transfer between components in a distributed system.

SQS helps to move data between distributed application modules without directly connecting them.

AWS documentation: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/Welcome.html

This module implements fully asynchronous access to SQS API in Python.

API documentation
-----------------

.. autoclass:: asyncaws.SQS
   :members:


.. _ReceiveMessage: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html
.. _SendMessage: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html
.. _DeleteMessage: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessage.html
.. _CreateQueue: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html
.. _DeleteQueue: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteQueue.html
.. _GetQueueAttributes: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_GetQueueAttributes.html
.. _SetQueueAttributes: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SetQueueAttributes.html
.. _AddPermission: http://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_AddPermission.html
