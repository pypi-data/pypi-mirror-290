# -*- coding: utf-8 -*-
# flake8: noqa

from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST
from utils import generate_order_id


supplier_no = 'spark2c'
with open("spark2c.key", 'rb') as pem_file:
    private_key = pem_file.read()
with open("spark.pub", 'rb') as pem_file:
    rsa_public_key = pem_file.read()

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))   #, host=SANDBOX_API_HOST)

ret, info = client.list_traffic_usages(username="200001", start_time="2024-07-08 23:59:59", end_time="2024-07-21 23:59:59", type="days")
print(ret)
print(info)