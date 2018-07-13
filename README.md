#HyAlipayApi

##项目简介
#####HyAliapyApi主要用于支付宝账户的账单查询与账单文件下载，此API一共三个方法！
>1、根据时间范围或默认时间范围下载文件，若不设定时间，默认下载当天账单。
>2、根据交易流水号或商户订单号或时间范围查询对应订单信息。若不设定时间，默认查询为以当前时间一周之前的账单。
>3、查询账户余额。

##安装方式：python setup.py install

##使用实例

```python

from hy_alipay_sdk import aliapy_api

class AlipayApi(object):
    def __init__(self, account, alipay_id, cookies,proxies_url,proxies_seller, filename=None):
        '''
        :param account:账号
        :param alipay_id: 账号ID
        :param cookies: cookies
        :param proxies_url: 代理地址
        :param proxies_seller: 代理类型
        
        :param filename: 下载文件时需要传入路径，给文件一个临时存储位置，最后读取文件并删除！
        '''
        self.account = account
        self.alipay_id = alipay_id
        self.cookies = cookies
        self.filename = filename    
        self.proxies_url = proxies_url    
        self.proxies_seller = proxies_seller    
        
    def download_file(proxies, start_time=None, end_time=None, input_charset='gbk'):
        '''
        :param proxies: 代理
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param input_charset: 编码方式
        :return file content
        '''
        return content
    
    def search_by_trade_no_or_trans_id(proxies, trade_no, start_time=None, end_time=None):
        '''
        :param proxies: 代理
        :param trade_no: 流水号
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return:parse content
        '''
        return parse content
    
    
    
    def get_balance(self, proxies):
        '''
        :param proxies: 代理
        :return: 剩余金额
        '''
        return money
    
if __name__ == '__main__':
    aliapy_api.AlipayApi(account, alipay_id, cookies,proxies_url,proxies_seller,'c:/hy_alipay_sdk/').download_file(proxies,'2018-07-10','2018-07-11','gbk')
    aliapy_api.AlipayApi(account, alipay_id, cookies,proxies_url,proxies_seller).search_by_trade_no_or_trans_id(proxies,trade_no,'2018-07-10','2018-07-11')
    aliapy_api.AlipayApi(account, alipay_id, cookies,proxies_url,proxies_seller).get_balance(proxies)
    
```        


#返回参数处理

## 通用异常返回结果

```
 {
                "apiVersion": "1.0",
                "error": {
                    "message": '输入参数为空',
                    "code": 10001,
                    "errors": 'null'
                }
            }
```

####download_file
```
{
    "file_content": [#账号：tbpek0501@163.com[20882218414870830156]\n", "#查询起始日期：2018-07-12 00:00:00查询终止日期：2018-07-13 00:00:00\n]
        
}
```

####search_by_trans_id_or_trade_no
```
{
    "content": [{
        "trade_no": "订单号",
        "business_serial_number": " 交易号",
        "amount": "金额",
        "counterparty": "对方",
        "created": "创建时间",
        "record_type_desc": "状态",
        "product_name": "",
        "accounts_serial_number": "交易号"
    }]
}
```
  
  
####get_balance

```
{'money': '173967.59'}
```


##项目结构
hy_alipay_sdk:  
│  
│  
│  MANIFEST.in  
│  README  
│  README.md  
│  requirements.txt  
│  setup.cfg  
│  setup.py  
│  test-requirements.txt  
│  tox.ini  
│    
│        
├─hy_alipay_sdk  
│      aliapy_api.py  
│      headers.py  
│      httpclient.py  
│      utils.py  
│      zipfileadd.py  
│      __init__.py  
│        
└─tests  
        cli.py  
        _test.py  
        __init__.py  