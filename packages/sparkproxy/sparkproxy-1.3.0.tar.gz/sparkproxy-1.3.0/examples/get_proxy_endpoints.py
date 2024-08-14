# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))   #, host=DEV_API_HOST)

# 获取订单&实例信息
ret, info = client.get_proxy_endpoints("USA")
print(ret)
print(info)
