#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import json
import re
import time
import logging
import datetime
import zipfileadd
import os
import requests
from lxml import etree
from hy_alipay_sdk.httpclient import HTTPClient
from hy_alipay_sdk.headers import *
from urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
t = time.time()
nowTime = lambda: int(round(t * 1000))
SEARCH_URL = 'https://consumeprod.alipay.com/record/advanced.htm'
DOWN_FILE_JSON_URL = "https://mbillexprod.alipay.com/enterprise/entAsyncSecurityCheck.json"
DOWN_ZIP_FILE_URL = "https://mbillexprod.alipay.com/enterprise/fundAccountDetailSyncDownload.resource?_t={0}&queryEntrance=1&billUserId=2088221841487083&showType=0&type=&precisionQueryKey=tradeNo&startDateInput={1}%2000:00:00&endDateInput={2}%2000:00:00&forceAync=0&downloadType=CSV&securityBizType=SECURITY_PRODUCT_ACCOUNT&securityId={3}"



class AlipayApi(object):
    def __init__(self, account, alipay_id, cookies, proxies_url,proxies_seller,filename=None):
        self.account = account
        self.alipay_id = alipay_id
        self.cookies = cookies
        self.filename = filename
        self.proxies_url=proxies_url
        self.proxies_seller=proxies_seller

    def download_file(self, proxies, start_time=None, end_time=None, input_charset='gbk'):

        '''
        :param proxies: 代理
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param input_charset: 编码方式

        '''
        try:
            # 设定默认时间
            START_TIME = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min).strftime(
                '%Y-%m-%d')
            END_TIME = datetime.datetime.combine(
                datetime.date.today() - datetime.timedelta(days=-1),
                datetime.time.min).strftime(
                '%Y-%m-%d')
            # 如果未传入时间参数则使用默认时间，否则使用传入的时间参数
            if start_time == None or end_time == None:
                start_time = START_TIME
                end_time = END_TIME
            else:
                start_time = start_time
                end_time = end_time

            DOWN_FILE_JSON_DATA = {'securityBizType': 'SECURITY_PRODUCT_ACCOUNT',
                                   'beginDate': start_time,
                                   'endDate': end_time,
                                   '_input_charset': input_charset
                                   }
            # 初始化对象
            INIT = HTTPClient(self.proxies_url, self.proxies_seller, self.cookies, proxies)
            # 请求下载之前的JSON地址得到securityId
            req_down_file_json = INIT.request('POST', DOWN_FILE_JSON_URL, data=DOWN_FILE_JSON_DATA,
                                              headers=DOWN_FILE_JSON_HEADERS)

            # 下载文件
            down_file = INIT.request('GET', DOWN_ZIP_FILE_URL.format(nowTime(), start_time, end_time,
                                                                     req_down_file_json.json()['securityId']), headers=DOWN_FILE_HEADERS)
            self.down_zip_file(down_file.content)
            dict={'file_content':self.unzip_file()}
            return json.dumps(dict, encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
        except Exception as e:
            return {
                    "apiVersion": "1.0",
                    "error": {
                        "message": e,
                        "code": 10001,
                        "errors": 'null'
                    }
                }

    def search_by_trade_no_or_trans_id(self, proxies, trade_no, start_time=None, end_time=None):
        '''
        :param proxies: 代理
        :param trade_no: 流水号
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return:parse content
        '''
        try:
            START_TIME = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min).strftime('%Y.%m.%d')
            END_TIME = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=6),
                                                 datetime.time.min).strftime('%Y.%m.%d')
            if start_time == None or end_time == None:
                start_date = START_TIME
                end_date = END_TIME
            else:
                timeTuple = time.strptime(start_time, "%Y-%m-%d")
                timeTuple_end = time.strptime(end_time, "%Y-%m-%d")
                start_date = time.strftime("%Y.%m.%d", timeTuple)
                end_date = time.strftime("%Y.%m.%d", timeTuple_end)
            SEARCH_DATA = {
                'rdsToken': '',
                'rdsUa': '',
                'beginDate': start_date,
                'beginTime': '00:00',
                'endDate': end_date,
                'endTime': '24:00',
                'dateRange': 'sevenDays',
                'status': 'all',
                'keyword': 'bizNo',
                'keyValue': trade_no,
                'dateType': 'createDate',
                'minAmount': '',
                'maxAmount': '',
                'fundFlow': 'all',
                'tradeType': 'ALL',
                'categoryId': '',
                'pageNum': '1'
            }

            get_total = HTTPClient(self.proxies_url, self.proxies_seller, self.cookies, proxies).request('POST',
                                                                                               SEARCH_URL,
                                                                                               data=SEARCH_DATA,
                                                                                               headers=SEARCH_HEADERS)
            dict={'content':self.spider(get_total)}


            return json.dumps(dict, encoding="UTF-8", ensure_ascii=False, sort_keys=False)
        except Exception as e:
            return {
                "apiVersion": "1.0",
                "error": {
                    "message": e,
                    "code": 10001,
                    "errors": 'null'
                }
            }

    def spider(self, get_total):
        '''
        Parse page
        :param get_total: response
        :return: content
        '''
        try:
            response = etree.HTML(get_total.text)
            created_data = response.xpath('//p[@class="time-d"]/text()')
            created_time = response.xpath('//p[@class="time-h ft-gray"]/text()')
            trade_nos = response.xpath('//td[@class="tradeNo ft-gray"]/p/text()')
            product_name = response.xpath('//p[@class="consume-title"]/a/text()')
            amount = response.xpath('//td[@class="amount"]/span/text()')
            counterparty = response.xpath('//p[@class="name"]/text()')
            record_type_desc = response.xpath('//td[@class="status"]/p/text()')
            content = []
            for i in range(0, len(trade_nos)):
                dict = {
                    'created': re.sub('\t|\n|\r|', '', created_data[i] + ' ' + created_time[i]),
                    'trade_no': trade_nos[i].split('|')[0],
                    'business_serial_number': trade_nos[i].split('|')[1].split('_')[0],
                    'product_name': product_name[i],
                    'amount': ''.join(amount[i]),
                    'counterparty': re.sub('\t|\n|\r|', '', counterparty[i]),
                    'record_type_desc': record_type_desc[i],
                    'accounts_serial_number': trade_nos[i].split('|')[1]
                }
                content.append(dict)
            return content
        except Exception as e:
            return {
                "apiVersion": "1.0",
                "error": {
                    "message": e,
                    "code": 10001,
                    "errors": 'null'
                }
            }
    def get_balance(self, proxies):
        '''
        Get balance
        :param proxies: proxies
        :return: money
        '''
        try:
            START_TIME = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min).strftime('%Y.%m.%d')
            END_TIME = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=6),
                                                 datetime.time.min).strftime('%Y.%m.%d')
            SEARCH_DATA = {
                'rdsToken': '',
                'rdsUa': '',
                'beginDate': START_TIME,
                'beginTime': '00:00',
                'endDate': END_TIME,
                'endTime': '24:00',
                'dateRange': 'sevenDays',
                'status': 'all',
                'keyword': 'bizNo',
                'keyValue': '',
                'dateType': 'createDate',
                'minAmount': '',
                'maxAmount': '',
                'fundFlow': 'all',
                'tradeType': 'ALL',
                'categoryId': '',
                'pageNum': '1'
            }
            get_total = HTTPClient(self.proxies_url, self.proxies_seller, self.cookies, proxies).request('POST',
                                                                                               SEARCH_URL,
                                                                                               data=SEARCH_DATA,
                                                                                               headers=SEARCH_HEADERS)

            response = etree.HTML(get_total.text)

            money = response.xpath('//em[@class="ft-green"]/strong/text()')
            return {'money':''.join(money)}
        except Exception as e:
            return {
                "apiVersion": "1.0",
                "error": {
                    "message": e,
                    "code": 10001,
                    "errors": 'null'
                }
            }


    def down_zip_file(self, content):
        '''
        :param content:file content
        '''

        try:
            with open(self.filename + str(self.alipay_id) + str('.zip'), 'wb')as f:
                f.write(content)
                f.close()
        except Exception as e:
            return {
                "apiVersion": "1.0",
                "error": {
                    "message": e,
                    "code": 10001,
                    "errors": 'null'
                }
            }

    def unzip_file(self):

        '''
        decompression.

        '''
        try:
            content = []
            try:
                zip_file_path = self.filename + str(self.alipay_id) + str('.zip')
                zfile = zipfileadd.ZipFile(zip_file_path, 'r')
                for csv_file_name in zfile.namelist():
                    zfile.extract(csv_file_name, self.filename)
                    filename_path = unicode(self.filename + csv_file_name.encode('utf-8'), "utf8")
                    f = codecs.open(filename_path, 'r', 'gbk')
                    text = f.readlines()
                    for i in text:
                        content.append(i)
                    f.close()
                    zfile.close()
                    os.remove(filename_path)
                    os.remove(zip_file_path)

            except Exception as e:
                logging.error("002-压缩包读取失败，请检查%s" % e)
            return content
        except Exception as e:
            return {
                "apiVersion": "1.0",
                "error": {
                    "message": e,
                    "code": 10001,
                    "errors": 'null'
                }
            }

