#!/usr/bin/env python

from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat
from core import AWSRequest


class SNS(object):
    def __init__(self, access_key, secret_key, region):
        self.region = region
        self.__access_key = access_key
        self.__secret_key = secret_key
        self._http = AsyncHTTPClient()

    def create_topic(self, name):
        params = {
            "Name": name,
            "Action": "CreateTopic",
            "Version": "2010-03-31",
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": 4,
        }
        url = "http://sns.{region}.amazonaws.com/".format(region=self.region)
        full_url = url_concat(url, params)
        request = AWSRequest(full_url,
                             service='sns',
                             region=self.region,
                             access_key=self.__access_key,
                             secret_key=self.__secret_key)
        return self._http.fetch(request,  raise_error=False)
