#!/usr/bin/env python

from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClient
from tornado.httputil import url_concat
import datetime
import hashlib
import hmac


class SQSRequest(HTTPRequest):
    """SQS AWS Adapter for Tornado HTTP request"""
    def __init__(self, *args, **kwargs):
        t = datetime.datetime.utcnow()
        method = kwargs.get('method', 'GET')
        url = kwargs.get('url') or args[0]
        params = sorted(url.split('?')[1].split('&'))
        canonical_querystring = '&'.join(params)
        kwargs['url'] = url.split('?')[0] + '?' + canonical_querystring
        args = tuple()
        host = url.split('://')[1].split('/')[0]
        canonical_uri = url.split('://')[1].split('.com')[1].split('?')[0]
        service = 'sqs'
        region = kwargs.get('region', 'eu-west-1')
        super(SQSRequest, self).__init__(*args, **kwargs)

