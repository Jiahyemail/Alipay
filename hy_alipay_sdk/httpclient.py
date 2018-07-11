# -*- coding: utf-8 -*-
import functools
import logging
import re
import ssl
import time
import requests
import urllib

from urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# logger = logging.getLogger(__name__)
from hy_alipay_sdk.utils import get_proxies


class HTTPClient(object):
    """Base http client wrapper."""

    def __init__(self, uri, seller, cookies=None, proxies=None):
        self.cookies = cookies
        self.cp_info = {}
        self.proxies = proxies
        self.session = requests.Session()
        self.timeout = 120
        self.uri = uri
        self.seller = seller

    def encode_params(self, url, data):
        if isinstance(data, dict):
            temp_data = []
            for k, v in data.items():
                temp_data.append((k, v))
            data = urllib.urlencode(temp_data)
        # logger.info('%s request data: %s', url, data.decode('utf8'))
        # logger.info('%s request data: %s', url, data)
        return data



    def wrap_exception(reraise=True):
        def inner(f):
            def wrapped(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logging.error(e.message)
                    if reraise:
                        raise e
                except Exception as e:
                    msg = 'Unexpected Exception: %s' % e.message
                    logging.critical(msg, exc_info=True)
                    if reraise:
                        new_e = Exception(u'未知错误，请联系技术')
                        raise new_e

            return functools.wraps(f)(wrapped)

        return inner

    def request(self, method, url, delay=0, max_retry=3, **kwargs):
        """
        http request retry.
        """

        kwargs['verify'] = False
        kwargs['allow_redirects']=False
        kwargs['cookies'] = self.cookies


        if not kwargs.get('timeout', None):
            kwargs['timeout'] = self.timeout

        if kwargs.get('data', None):
            data = kwargs.get('data')
            data = self.encode_params(url, data)

        if kwargs.get('params', None):
            params = kwargs.get('params')
            params = self.encode_params(url, params)
        else:
            params = ""

        if self.proxies and not kwargs.get('proxies'):
            kwargs['proxies'] = self.proxies

        time.sleep(delay)

        def get_new_proxy():
            new_proxy = get_proxies(self.uri, self.seller)
            kwargs['proxies'] = new_proxy
            logging.info('GET NEW PROXIES (client) %s', self.proxies)

        retry = 0
        exc_obj = None
        for _ in range(max_retry):
            try:
                # print(kwargs)
                response = requests.request(method, url,**kwargs)
                return response
            except (requests.exceptions.Timeout,
                    requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ChunkedEncodingError,
                    ssl.SSLError) as e:
                    logging.info("%s, retry after 1 seconds.", e.message)
                    # print(e)
                    time.sleep(1)
                    retry += 1
                    if u'005-Cannot connect to proxy' in str(e.message):
                        get_new_proxy()

                    ip_list = re.findall(ur"Connection to (.*) timed out", str(e.message))
                    if ip_list:
                        error_ip = ip_list[0]
                        if kwargs.get('proxies') and error_ip in str(kwargs.get('proxies')):
                            get_new_proxy()

                    logging.error("After %s retries still got %s, give up.",
                                 retry, e.message)
                    if 'Connection aborted' in str(e.message):
                        exc_obj = Exception(u'003-访问被拒绝, %s' % str(kwargs.get('proxies')))

                    if u'005-Cannot connect to proxy' in str(e.message):
                        ip_list = re.findall(ur"Connection to (.*) timed out", str(e.message))
                        if ip_list:
                            error_ip = ip_list[0]
                            exc_obj = Exception(u'proxy无法访问, [%s]' % error_ip)
                        else:
                            exc_obj = Exception(e.message)

                    ip_list = re.findall(ur"Connection to (.*) timed out", str(e.message))
                    if ip_list:
                        error_ip = ip_list[0]
                        logging.info('error_ip, %s', str(error_ip))
                        if error_ip in url:
                            logging.info('host error_ip, %s', str(error_ip))
                            exc_obj = Exception(u'host访问超时, [%s]' % error_ip)
                        elif kwargs.get('proxies') and error_ip in str(kwargs.get('proxies')):
                            logging.info('proxy error_ip, %s', str(error_ip))
                            exc_obj = Exception(u'proxy访问超时, [%s]' % error_ip)

                    exc_obj = Exception(u'004-访问超时, %s' % e.message)
                    continue

        raise exc_obj


