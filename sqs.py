from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClient
from tornado.httputil import url_concat
import datetime
import hashlib
import hmac


class SQSRequest(HTTPRequest):
    """SQS AWS Adapter for Tornado HTTP request"""
    def __init__(self, *args, **kwargs):
        super(SQSRequest, self).__init__(*args, **kwargs)

