#HyAlipayApi

##项目简介
#####HyAliapyApi主要用于支付宝账户的账单查询与账单文件下载，此API一共三个方法！
>1、根据时间范围或默认时间范围下载文件，若不设定时间，默认下载当天账单。<br/>
>2、根据交易流水号或商户订单号或时间范围查询对应订单信息。若不设定时间，默认查询为以当前时间一周之前的账单。<br/>
>3、查询账户余额。<br/>

##安装方式：python setup.py install

##使用实例
```python
from hy_alipay_sdk import aliapy_api

class AlipayApi(object):
    def __init__(self, account, alipay_id, cookies, filename=None):
        '''
        :param account:账号
        :param alipay_id: 账号ID
        :param cookies: cookies
        :param filename: 下载文件时需要传入路径，给文件一个临时存储位置，最后读取文件并删除！
        '''
        self.account = account
        self.alipay_id = alipay_id
        self.cookies = cookies
        self.filename = filename    
        
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
    aliapy_api.AlipayApi(account, alipay_id, cookies,'c:/hy_alipay_sdk/').download_file(proxies,'2018-07-10','2018-07-11','gbk')
    aliapy_api.AlipayApi(account, alipay_id, cookies).search_by_trade_no_or_trans_id(proxies,trade_no,'2018-07-10','2018-07-11')
    aliapy_api.AlipayApi(account, alipay_id, cookies).get_balance(proxies)
    
```        
##ERROR
>1、003-访问被拒绝<br/>
>2、004-访问超时<br/>
>3、005-Cannot connect to proxy<br/>
以上属于连接是发生的错误，程序会进行重试，在重试三次若无效，程序会停止运行。应检查代理IP是否有效，网站结构是否更改！<br/>
>4、001-下载压缩包失败,请检查<br/>
>5、002-压缩包读取失败，请检查<br/>
检查文件是否下载，下载后的ZIP是否为正常文件<br/>

#return
####download_file<br/>
  >>return ["#账号：tbpek0501@163.com[20882218414870830156]\n", "#查询起始日期：2018-07-11 00:00:00查询终止日期：2018-07-12 00:00:00\n"]<br/>
  若失败则 return [] or 001 or 002 error

####search_by_trans_id_or_trade_no<br/>
  >>return [
  {
    'created': 创建时间，
    'trade_no': 订单号,
    'business_serial_number': 交易号,
    'product_name': 名称,
    'income_amount': 金额,
    'counterparty': 对方,
    'status': 状态
  }
  ]
  若失败则 return[] or 003 or 004 or 005
  

####get_balance
  >>return float(balance) or None


##项目结构
hy_alipay_sdk:<br/>
│<br/>
│<br/>
│  MANIFEST.in<br/>
│  README<br/>
│  README.md<br/>
│  requirements.txt<br/>
│  setup.cfg<br/>
│  setup.py<br/>
│  test-requirements.txt<br/>
│  tox.ini<br/>
│  <br/>
│     <br/> 
├─hy_alipay_sdk<br/>
│      aliapy_api.py<br/>
│      headers.py<br/>
│      httpclient.py<br/>
│      utils.py<br/>
│      zipfileadd.py<br/>
│      __init__.py<br/>
│      <br/>
└─tests
        cli.py<br/>
        _test.py<br/>
        __init__.py<br/>