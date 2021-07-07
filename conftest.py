#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

from base.method import My_request
import pytest
import json
from utils.operationExcel import OperationExcel



'''
获获取全局token,测试用例用到直接调用方法名即可
'''

# 获取url前缀，更新环境
caseUrl = OperationExcel(filename="data.xls", sheet="parse").get_data()[0][OperationExcel.caseUrl]
new_prefix = caseUrl.split(".")[0]

# 获取修理厂token
@pytest.fixture(scope="session")
def repair_shopToken():
    json = {"phone":"20000000000","password":"0170ce7e5932cee53d10d6f7bb6eba0f","type":"kangaroo-parts-web","captchaKey":"","captchaValue":"","grant_type":"password","scope":"all"}

    obj = My_request()
    r = obj.POST(
        url=  "{0}.daishupei.com/api/auth/oauth/login".format(new_prefix),
        headers = {"Authorization":"Basic a2FuZ2Fyb28tcGFydHMtd2ViOnREd2ZRYVBhJWVESXN0Vzk="},
        json = json
    )
    token = r.json()["data"]["value"]
    return "Bearer {0}".format(token)

# 获取供应商token
@pytest.fixture(scope="session")
def supplierToken():
    json = {"phone":"30000000000","password":"0170ce7e5932cee53d10d6f7bb6eba0f","type":"kangaroo-parts-web","captchaKey":"","captchaValue":"","grant_type":"password","scope":"all"}
    obj = My_request()
    r = obj.POST(
        url= "{0}.daishupei.com/api/auth/oauth/login".format(new_prefix),
        headers = {"Authorization":"Basic a2FuZ2Fyb28tcGFydHMtd2ViOnREd2ZRYVBhJWVESXN0Vzk="},
        json = json
    )
    token = r.json()["data"]["value"]
    return "Bearer {0}".format(token)
