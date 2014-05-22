from tornado.httpclient import AsyncHTTPClient, HTTPClient
from tornado.httputil import url_concat
from lxml import objectify
from core import AWSRequest


class SNS(object):
    def __init__(self, access_key, secret_key, region, async=True):
        self.region = region
        self.__access_key = access_key
        self.__secret_key = secret_key
        self._http = AsyncHTTPClient() if async else HTTPClient()
        self.service = 'sns'
        self.common_params = {
            "Version": "2010-03-31",
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": 4
        }

    @staticmethod
    def parse(response):
        """
        Parse XML string response from AWS and return Python value
        :param resp: raw aws response string
        :return: Python string, boolean or None
        """
        response_mapping = {
            'CreateTopicResult': lambda x: x.CreateTopicResult.TopicArn,
            'SubscribeResult': lambda x: x.SubscribeResult.SubscriptionArn
        }
        root = objectify.fromstring(response)
        for key, extract_func in response_mapping.items():
            if hasattr(root, key):
                return extract_func(root)
        return None

    def create_topic(self, name):
        """
        Creates a topic to which notifications can be published.
        This action is idempotent, so if the requester already owns
        a topic with the specified name, that topic's ARN
        is returned without creating a new topic.
        http://docs.aws.amazon.com/sns/latest/APIReference/API_CreateTopic.html
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
        full_url = url_concat(url, params)
        request = AWSRequest(full_url, service=self.service, region=self.region,
                             access_key=self.__access_key,
                             secret_key=self.__secret_key)
        return self._http.fetch(request)

    def subscribe(self, endpoint, topic_arn, protocol):
        """
        Prepares to subscribe an endpoint by sending the endpoint
        a confirmation message. To actually create a subscription,
        the endpoint owner must call the ConfirmSubscription action
        with the token from the confirmation message.
        http://docs.aws.amazon.com/sns/latest/APIReference/API_Subscribe.html
        :param endpoint: The endpoint to receive notifications.
        :param topic_arn: The ARN of the topic to subscribe to.
        :param protocol: The protocol to use (http, email, sms, sqs etc)
        :return: ARN of the subscription, if the service was able to create it
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
        full_url = url_concat(url, params)
        request = AWSRequest(full_url, service=self.service, region=self.region,
                             access_key=self.__access_key,
                             secret_key=self.__secret_key)
        return self._http.fetch(request)

    def confirm_subscription(self, topic_arn, token):
        """
        Verifies an endpoint owner's intent to receive messages by validating
        the token sent to the endpoint by an earlier Subscribe action.
        If the token is valid, the action creates a new subscription
        and returns its Amazon Resource Name (ARN)
        :param topic_arn: The ARN of the topic for subscription.
        :param token: Short-lived token returned during the Subscribe action.
        :return: SubscriptionArn - The ARN of the created subscription.
        """
        params = {
            "TopicArn": topic_arn,
            "Token": token,
            "Action": "ConfirmSubscription"
        }
        params.update(self.common_params)
        url = "http://{service}.{region}.amazonaws.com/".format(
            service=self.service, region=self.region)
        full_url = url_concat(url, params)
        request = AWSRequest(full_url, service=self.service, region=self.region,
                             access_key=self.__access_key,
                             secret_key=self.__secret_key)
        return self._http.fetch(request)
