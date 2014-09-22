"""Module that covers SNS API"""
from asyncaws.core import AWS
import json


class SNS(AWS):
    """
    :param access_key: AWS_ACCESS_KEY_ID
    :param secret_key: AWS_SECRET_ACCESS_KEY
    :param region: region name as string
    :param async: True by default, indicates that AsyncHTTPClient should
        be used. Otherwise HTTPClient (synchronous). Useful for debugging.
    """
    common_params = {
        "Version": "2010-03-31",
    }
    service = 'sns'

    def create_topic(self, name):
        """
        Creates a topic to which notifications can be published.
        This action is idempotent, so if the requester already owns
        a topic with the specified name, that topic's ARN
        is returned without creating a new topic.
        AWS API: CreateTopic_

        :param name: The name of the topic to create.
        :return: TopicArn - The Amazon Resource Name assigned to the topic.
        """
        params = {
            "Name": name,
            "Action": "CreateTopic"
        }
        params.update(self.common_params)
        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        parse_function = lambda root: root.CreateTopicResult.TopicArn.text
        return self._process(url, params, self.service, parse_function)

    def delete_topic(self, topic_arn):
        """
        Deletes a topic and all its subscriptions.
        Deleting a topic might prevent some messages previously sent to the
        topic from being delivered to subscribers. This action is idempotent,
        so deleting a topic that does not exist does not result in an error.
        AWS API: DeleteTopic_

        :param topic_arn: The ARN of the topic to delete
        :return: RequestId
        """
        params = {
            "TopicArn": topic_arn,
            "Action": "DeleteTopic"
        }
        params.update(self.common_params)
        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        parse_function = lambda root: root.ResponseMetadata.RequestId.text
        return self._process(url, params, self.service, parse_function)

    def subscribe(self, endpoint, topic_arn, protocol):
        """
        Prepares to subscribe an endpoint by sending the endpoint
        a confirmation message. To actually create a subscription,
        the endpoint owner must call the ConfirmSubscription action
        with the token from the confirmation
        AWS API: Subscribe_

        :param endpoint: The endpoint to receive notifications.
        :param topic_arn: The ARN of the topic to subscribe to.
        :param protocol: The protocol to use (http, email, sms, sqs etc)
        :return: SubscriptionARN, if the service was able to create it
            immediately (without requiring endpoint owner confirmation).

        """
        params = {
            "Endpoint": endpoint,
            "Protocol": protocol,
            "TopicArn": topic_arn,
            "Action": "Subscribe"
        }
        params.update(self.common_params)
        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        parse_function = lambda root: root.SubscribeResult.SubscriptionArn.text
        return self._process(url, params, self.service, parse_function)

    def confirm_subscription(self, topic_arn, token, auth_unsubscribe=False):
        """
        Verifies an endpoint owner's intent to receive messages by validating
        the token sent to the endpoint by an earlier Subscribe action.
        If the token is valid, the action creates a new subscription
        and returns its Amazon Resource Name (ARN).
        AWS API: ConfirmSubscription_

        :param topic_arn: The ARN of the topic for subscription.
        :param token: Short-lived token returned during the Subscribe action.
        :param auth_unsubscribe: Boolean, disallows unauthenticated
               unsubscribes of the subscription.
        :return: SubscriptionArn - The ARN of the created subscription.
        """
        params = {
            "TopicArn": topic_arn,
            "Token": token,
            "Action": "ConfirmSubscription",
            "AuthenticateOnUnsubscribe": str(auth_unsubscribe).lower()
        }
        params.update(self.common_params)
        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        parse_func = lambda r: r.ConfirmSubscriptionResult.SubscriptionArn.text
        return self._process(url, params, self.service, parse_func)

    def publish(self, message, subject, topic_arn, target_arn=None,
                message_structure=None):
        """
        Sends a message to all of a topic's subscribed endpoints.
        When a messageId is returned, the message has been saved and SNS
        will attempt to deliver it to the topic's subscribers shortly.
        The format of the outgoing message to each subscribed endpoint depends
        on the notification protocol selected.
        AWS API: Publish_

        :param message: The message to send to the topic.  To send the same
            message to all transport protocols, include the text of the message
            as a String value. To send different messages for each transport
            protocol, set the value of the MessageStructure parameter to json
            and use a JSON object for the Message parameter. If Python list or
            dict is passed, it will be converted to json automatically.
        :param subject: Optional parameter to be used as the "Subject" line
            when the message is delivered to email endpoints.
        :param topic_arn: The topic to publish to.
        :param target_arn: Either TopicArn or EndpointArn, but not both.
        :param message_structure: Should be empty to send the same message to
            all protocols, or "json" to send a different messages.
        :return: MessageId - Unique identifier assigned to the published message
        """
        assert message_structure in (None, 'json')
        assert topic_arn or target_arn
        params = {
            "Message": message,
            "Subject": subject,
            "Action": "Publish"
        }
        # convert message to json if needed
        if message_structure == 'json':
            if not isinstance(message, (str, unicode)):
                params['Message'] = json.dumps(message)
            params['MessageStructure'] = message_structure
        # set topic_arn or target_arn
        if topic_arn:
            params["TopicArn"] = topic_arn
        else:
            params["TargetArn"] = target_arn
        params.update(self.common_params)
        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        parse_function = lambda root: root.PublishResult.MessageId.text
        return self._process(url, params, self.service, parse_function)
