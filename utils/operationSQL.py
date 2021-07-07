#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pymysql
from utils.operationConfig import get_configparser
from utils.operationExcel import OperationExcel

def get_connSql(SQL):
    caseUrl = OperationExcel(filename="data.xls", sheet="parse").get_data()[0][OperationExcel.caseUrl]
    new_prefix = caseUrl.split(".")[0]
    data = get_configparser(new_prefix)
    conn = pymysql.connect(
        host=data["ip"],
        user=data["user"],
        port=int(data["port"]),
        password=data["password"],
        db = "kangaroo_parts"
    )
    # 创建游标对象
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(SQL)
    return cursor.fetchall()


# sql = "select *from quote_main where inquiry_id = '1407305867162406913';"
# print(get_connSql(sql))


