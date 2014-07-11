import json
import hashlib
from core import AWS


class SQS(AWS):
    """
    :param access_key: AWS_ACCESS_KEY_ID
    :param secret_key: AWS_SECRET_ACCESS_KEY
    :param region: region name as string
    :param async: True by default, indicates that AsyncHTTPClient should
        be used. Otherwise HTTPClient (synchronous). Useful for debugging.
    """
    service = 'sqs'
    common_params = {"Version": "2012-11-05"}

    def listen_queue(self, queue_url, wait_time=15, max_messages=1,
                     visibility_timeout=300):
        """
        Retrieves one or more messages from the specified queue.
        Long poll support is enabled by using the WaitTimeSeconds parameter.
        AWS API: ReceiveMessage_

        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :param wait_time: The duration (in seconds) for which the call will
            wait for a message to arrive in the queue before returning.
            If a message is available, the call will return sooner.
        :param max_messages: The maximum number of messages to return.
        :param visibility_timeout: The duration (in seconds) that the received
            messages are hidden from subsequent retrieve requests after being
            retrieved by a ReceiveMessage request.
        :return: A message or a list of messages.
        """
        def parse_function(root):
            if root.ReceiveMessageResult == '':
                return None
            message = root.ReceiveMessageResult.Message
            result = {
                'Body': message.Body.text,
                'MD5OfBody': message.MD5OfBody.text,
                'ReceiptHandle': message.ReceiptHandle.text,
                'Attributes': {}
            }
            for attr in message.Attribute:
                result['Attributes'][attr.Name.text] = attr.Value.text
            return result

        params = {
            "Action": "ReceiveMessage",
            "WaitTimeSeconds": wait_time,
            "MaxNumberOfMessages": max_messages,
            "VisibilityTimeout": visibility_timeout,
            "AttributeName": "All",
        }
        params.update(self.common_params)
        return self._process(queue_url, params, self.service, parse_function)

    def send_message(self, queue_url, message_body):
        """
        Delivers a message to the specified queue.
        AWS API: SendMessage_

        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :param message_body: The message to send. String maximum 256 KB in size.
        :return: MD5OfMessageAttributes, MD5OfMessageBody, MessageId
        """
        params = {
            "Action": "SendMessage",
            "MessageBody": message_body,
        }
        params.update(self.common_params)
        parse_function = lambda root: root.SendMessageResult.MessageId.text
        return self._process(queue_url, params, self.service, parse_function)

    def delete_message(self, queue_url, receipt_handle):
        """
        Deletes the specified message from the specified queue.
        Specify the message by using the message's receipt handle, not ID.
        AWS API: DeleteMessage_

        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :param receipt_handle: The receipt handle associated with the message.
        :return: Request ID
        """
        params = {
            "Action": "DeleteMessage",
            "ReceiptHandle": receipt_handle,
        }
        params.update(self.common_params)
        parse_function = lambda res: res.ResponseMetadata.RequestId.text
        return self._process(queue_url, params, self.service, parse_function)

    def create_queue(self, queue_name, attributes={}):
        """
        Creates a new queue, or returns the URL of an existing one.
        To successfully create a new queue, a name that is unique within
        the scope of own queues should be provided.
        Beware: 60 seconds should pass between deleting a queue and creating
        another with the same name.
        AWS API: CreateQueue_

        :param queue_name: The name for the queue to be created.
        :return: QueueUrl - the URL for the created Amazon SQS queue.
        """
        params = {
            "Action": "CreateQueue",
            "QueueName": queue_name,
        }
        for i, (key, value) in enumerate(attributes):
            params['Attribute.%s.Name' % i] = key
            params['Attribute.%s.Value' % i] = value

        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        params.update(self.common_params)
        parse_function = lambda res: res.CreateQueueResult.QueueUrl.text
        return self._process(url, params, self.service, parse_function)

    def delete_queue(self, queue_url):
        """
        Deletes the queue specified by the queue URL, regardless of whether
        the queue is empty. If the specified queue does not exist, SQS
        returns a successful response.
        Beware: 60 seconds should pass between deleting a queue and creating
        another with the same name.
        AWS API: DeleteQueue_

        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :return: Request ID
        """
        params = {
            "Action": "DeleteQueue",
        }
        params.update(self.common_params)

        parse_function = lambda root: root.ResponseMetadata.RequestId.text
        return self._process(queue_url, params, self.service, parse_function)

    def get_queue_attributes(self, queue_url, attributes=('all',)):
        """
        Gets attributes for the specified queue.
        The following attributes are supported:

        All (returns all values), ApproximateNumberOfMessages,
        ApproximateNumberOfMessagesNotVisible,
        VisibilityTimeout, CreatedTimestamp, LastModifiedTimestamp, Policy,
        MaximumMessageSize, MessageRetentionPeriod, QueueArn,
        ApproximateNumberOfMessagesDelayed, DelaySeconds,
        ReceiveMessageWaitTimeSeconds, RedrivePolicy.

        AWS API: GetQueueAttributes_

        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :param attributes: A list of attributes to retrieve, ['all'] by default.
        :return: A map of attributes to the respective values.
        """
        params = {
            "Action": "GetQueueAttributes",
        }
        for i, attr in enumerate(attributes):
            params['AttributeName.%s' % (i + 1)] = attr
        params.update(self.common_params)

        def parse_function(root):
            result = {}
            for attr in root.GetQueueAttributesResult.Attribute:
                result[attr.Name.text] = attr.Value.text
            return result
        return self._process(queue_url, params, self.service, parse_function)

    def set_queue_attributes(self, queue_url, attributes={}):
        """
        Sets the value of one or more queue attributes.
        AWS API: SetQueueAttributes_

        :param attributes: dict of attribute names and values.
        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :return: Request ID
        """
        params = {
            "Action": "SetQueueAttributes",
        }
        for i, (key, value) in enumerate(attributes.items()):
            params['Attribute.%s.Name' % i] = key
            params['Attribute.%s.Value' % i] = value
        params.update(self.common_params)

        def parse_function(res):
            import ipdb;ipdb.set_trace()
        return self._process(queue_url, params, self.service, parse_function)

    def add_permission(self, queue_url, account_ids, action_names, label):
        """
        Adds a permission to a queue for a specific principal.
        This allows for sharing access to the queue.
        AWS API: AddPermission_

        :param queue_url: The URL of the Amazon SQS queue to take action on.
        :param account_ids: List of AWS account numbers to grant a permission.
        :param action_names: List of actions the client wants to allow for the
            specified principal. The following are valid values: *, SendMessage,
            ReceiveMessage, DeleteMessage, ChangeMessageVisibility,
            GetQueueAttributes, GetQueueUrl.
        :param label: The unique identification of the permission.
        :return: Request ID
        """
        params = {
            "Action": "AddPermission",
            "Label": label,
        }
        for i, acc_id in enumerate(account_ids):
            params['AWSAccountId.%s' % (i + 1)] = acc_id
        for i, name in enumerate(action_names):
            params['ActionName.%s' % (i + 1)] = name
        params.update(self.common_params)

        def parse_function(res):
            import ipdb;ipdb.set_trace()
        return self._process(queue_url, params, self.service, parse_function)

    # Helpers
    def allow_sns_topic(self, queue_url, queue_arn, topic_arn):
        """
        Helper method to grant the sns topic a permission for publishing
        messages to queue. Calls set_queue_attributes under the hood.

        :param queue_url: url of queue to get messages
        :param queue_arn: arn of queue to get messages
        :param topic_arn: arn of topic to publish messages
        :return: None
        """
        sid = hashlib.md5((topic_arn + queue_arn).encode('utf-8')).hexdigest()
        statement = {'Action': 'SQS:SendMessage',
                     'Effect': 'Allow',
                     'Principal': {'AWS': '*'},
                     'Resource': queue_arn,
                     'Sid': sid,
                     'Condition': {'StringLike': {'aws:SourceArn': topic_arn}}}
        policy = {'Version': '2008-10-17',
                  'Id': queue_arn + '/SQSDefaultPolicy',
                  'Statement': [statement]}
        return self.set_queue_attributes(queue_url,
                                         {"Policy": json.dumps(policy)})
