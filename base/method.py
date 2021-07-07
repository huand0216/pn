#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import requests

'''
二次封装request请求方法
'''
class My_request(object):
    def my_request(self,method,url,**kwargs):
        try:
            return requests.request(method=method,url=url,**kwargs)
        except BaseException as e:
            print(e.args)

    def POST(self,url,**kwargs):
        try:
            return requests.post(url=url,**kwargs)
        except BaseException as e:
            print(e.args)

    def GET(self,url,**kwargs):
        try:
            return requests.get(url=url,**kwargs)
        except BaseException as e:
            print(e.args)
