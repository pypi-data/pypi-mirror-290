# -*- coding: utf-8 -*-
# flake8: noqa
import time
import random

from utils import generate_order_id
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()
client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key, public_key=rsa_public_key), host="http://127.0.0.1:8081")

ret, info = client.init_proxy_user("user", "test")
order_no = generate_order_id()
ret, info = client.recharge_traffic(req_order_no=order_no, username="user", traffic=1000, validity_days=90)
print(ret)
print(info)

ret, info = client.get_traffic_record(req_order_no=order_no)
print(ret)
print(info)