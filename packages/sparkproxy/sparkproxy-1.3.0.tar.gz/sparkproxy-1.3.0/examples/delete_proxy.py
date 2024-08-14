# -*- coding: utf-8 -*-
# flake8: noqa
from utils import generate_order_id
from sparkproxy import Auth
from sparkproxy import SparkProxyClient
from sparkproxy.config import SANDBOX_API_HOST, DEV_API_HOST

supplier_no = 'test0001'
with open("key.pem", 'rb') as pem_file:
    private_key = pem_file.read()

client = SparkProxyClient(Auth(supplier_no=supplier_no, private_key=private_key))   #, host=DEV_API_HOST)

# 已生效、未过期的实例，可以续费
# ret, info = client.delete_proxy(req_order_no=generate_order_id(), instances=["90108d9ae44f4b83bf9566caff236aad"])
ret, info = client.delete_proxy(req_order_no='17202907918472920', instances=["123e0400b9b84398910edc3dc41f91df", "6a941adce65542e6983c9b0ce23cbf8f"])
ret, info = client.delete_proxy(req_order_no='17202909310467862', instances=["f25bc5b577374437a3dcca0e9614c698", "6bb4a461720e43529c25a19c86574218"])

print(ret)
print(info)
