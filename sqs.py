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

        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d')

        canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n'
        signed_headers = 'host;x-amz-date'
        payload_hash = hashlib.sha256('').hexdigest()

        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()
        signing_key = self.getSignatureKey(kwargs['secret_key'], datestamp, region, service)
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
        authorization_header = algorithm + ' ' + 'Credential=' + kwargs['access_key'] + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

        del kwargs['access_key']
        del kwargs['secret_key']
        headers = kwargs.get('headers', {})
        headers.update({'x-amz-date':amz_date, 'Authorization':authorization_header})
        kwargs['headers'] = headers
        super(SQSRequest, self).__init__(*args, **kwargs)

    def sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = self.sign(kDate, regionName)
        kService = self.sign(kRegion, serviceName)
        kSigning = self.sign(kService, 'aws4_request')
        return kSigning


