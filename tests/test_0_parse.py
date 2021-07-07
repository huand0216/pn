#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pytest
import os
import allure
from base.method import My_request
from utils.operationYaml import OperationYaml
from utils.operationExcel import OperationExcel,ExcelMappingYaml
from common.getpath import Public_path

'''
测试VIN解析和OE解析接口
'''

class TestParse(object):
    excelData = OperationExcel(filename="data.xls",sheet="parse").get_data()
    # yamlData = OperationYaml(filename="data.yaml").readYamlDict()

    # 测试VIN解析
    @pytest.mark.parametrize(
        "data",excelData
    )
    def test_parse001(self,data,repair_shopToken):
        url = data[OperationExcel.caseUrl]
        method = data[OperationExcel.caseMethod]
        parameter = data[OperationExcel.caseParameter]
        print(parameter)
        jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(parameter)
        expect = data[OperationExcel.caseExpect]
        if method == "POST":
            r = My_request().POST(url=url,
                                headers = {"Authorization":repair_shopToken},
                                json = jsonData
                                )
            assert r.status_code == 200
            assert expect in r.text
        elif method == "GET":
            r = My_request().GET(url=url,params=jsonData,
                                 headers={"Authorization":repair_shopToken}
                                 )
            assert r.status_code == 200
            assert expect in r.text

# if __name__ == '__main__':

    # pytest.main(["-v", "-s"])
    # pytest.main(["-v", "-s", "test_0_parse.py", "--alluredir", "./report/"])
    # import subprocess
    # subprocess.call('allure generate report/result/ -o report/html --clean', shell=True)
    # subprocess.call('allure open -h 127.0.0.1 -p 8088 ./report/html', shell=True)

    # os.system("allure generate ./temp -o ./report --clean")