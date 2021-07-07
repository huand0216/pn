#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pytest
import string
from base.method import My_request
from utils.operationExcel import OperationExcel,ExcelMappingYaml
from utils.operationYaml import OperationYaml
import random

class Test_others():
    excelData = OperationExcel(filename="data.xls",sheet="others").get_data()

    @pytest.mark.parametrize(
        "data",excelData
    )
    def test_others(self,data,repair_shopToken,supplierToken):
        # 获取到请求需要的参数
        caseId = data[OperationExcel.caseId]
        url = data[OperationExcel.caseUrl]
        method = data[OperationExcel.caseMethod]
        remark = data[OperationExcel.caseRemarks]
        operator = data[OperationExcel.caseOperator]
        parameter = data[OperationExcel.caseParameter]  # 参数
        expect = data[OperationExcel.caseExpect]

        if operator == "repair_shopToken":
            headers = {"Authorization": repair_shopToken}
        elif operator == "supplierToken":
            headers = {"Authorization": supplierToken}
        jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(parameter)
        if caseId == "case036":
            for i in range(3):
                jsonData["matchType"] = i+1
                res = My_request().POST(url=url, headers=headers, json=jsonData)
                result = res.text
        elif caseId == "case035":
            res = My_request().POST(url=url, headers=headers, params=jsonData)
            result = res.text
        elif caseId == "case038":
            random_int = random.randint(00000000000,99999999999)
            # 更新掉新增员工的手机号
            jsonData["phone"] = str(random_int)
            res = My_request().POST(url=url, headers=headers, json=jsonData)
            result = res.text
            # 更新case039、case040的参数
            del_id = res.json()["data"]
            modify_data = OperationYaml(filename="data.yaml").readYamlDict()
            modify_data["case039"]["id"] = del_id     # 更新成要删除的id
            modify_data["case040"]["oem"] = str(random_int)
            OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_data)   # 更新

        elif method == "GET":
            res = My_request().GET(url=url, headers=headers, params=jsonData)
            result = res.text
        elif method == "POST":
            res = My_request().POST(url=url, headers=headers, json=jsonData)
            result = res.text
            # 更新case035的参数
            if caseId == "case034":
                delDeliveryId = res.json()["data"]["orgDeliveryDTOS"][1]["id"]
                modify_data = OperationYaml(filename="data.yaml").readYamlDict()
                modify_data["case035"]["id"] = delDeliveryId
                OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_data)  # 更新
        # 对所有用例进行断言
        assert expect in result

if __name__ == '__main__':
    pytest.main(["-v","-s","test_others.py"])