from tornado.httpclient import HTTPRequest
from urlparse import urlparse
import datetime
import hashlib
import hmac


def sign(key, msg):
    """Make sha256 signature"""
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    """Sign all params sequentially"""
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


class AWSRequest(HTTPRequest):
    """
    Generic AWS Adapter for Tornado HTTP request
    Generates v4 signature and sets all required headers
    """
    def __init__(self, *args, **kwargs):
        service = kwargs['service']
        region = kwargs['region']
        method = kwargs.get('method', 'GET')
        url = kwargs.get('url') or args[0]
        # tornado url_concat encodes spaces as '+', but AWS expects '%20'
        url = url.replace('+', '%20')
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        canonical_uri = parsed_url.path
        # sort params alphabetically
        params = sorted(parsed_url.query.split('&'))
        canonical_querystring = '&'.join(params)
        kwargs['url'] = url.replace(parsed_url.query, canonical_querystring)
        # reset args, everything is passed with kwargs
        args = tuple()
        # prepare timestamps
        utc_time = datetime.datetime.utcnow()
        amz_date = utc_time.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = utc_time.strftime('%Y%m%d')
        # prepare aws-specific headers
        canonical_headers = 'host:{host}\nx-amz-date:{amz_date}\n'.format(
            host=host, amz_date=amz_date)
        signed_headers = 'host;x-amz-date'
        # for GET requests payload is empty
        payload_hash = hashlib.sha256('').hexdigest()

        canonical_request = (
            '{method}\n{canonical_uri}\n{canonical_querystring}'
            '\n{canonical_headers}\n{signed_headers}\n{payload_hash}'
        ).format(
            method=method, canonical_uri=canonical_uri,
            canonical_querystring=canonical_querystring,
            canonical_headers=canonical_headers, signed_headers=signed_headers,
            payload_hash=payload_hash
        )
        # creating signature
        algorithm = 'AWS4-HMAC-SHA256'
        scope = '{date_stamp}/{region}/{service}/aws4_request'.format(
            date_stamp=date_stamp, region=region, service=service)
        string_to_sign = '{algorithm}\n{amz_date}\n{scope}\n{hash}'.format(
            algorithm=algorithm, amz_date=amz_date, scope=scope,
            hash=hashlib.sha256(canonical_request).hexdigest())
        sign_key = get_signature_key(kwargs['secret_key'],
                                     date_stamp, region, service)
        hash_tuple = (sign_key, string_to_sign.encode('utf-8'), hashlib.sha256)
        signature = hmac.new(*hash_tuple).hexdigest()
        authorization_header = (
            '{algorithm} Credential={access_key}/{scope}, '
            'SignedHeaders={signed_headers}, Signature={signature}'
        ).format(
            algorithm=algorithm, access_key=kwargs['access_key'], scope=scope,
            signed_headers=signed_headers, signature=signature
        )
        # clean-up kwargs
        del kwargs['access_key']
        del kwargs['secret_key']
        del kwargs['service']
        del kwargs['region']
        # update headers
        headers = kwargs.get('headers', {})
        headers.update({'x-amz-date': amz_date,
                        'Authorization': authorization_header})
        kwargs['headers'] = headers
        # init Tornado HTTPRequest
        super(AWSRequest, self).__init__(*args, **kwargs)
