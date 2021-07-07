#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pytest
import string
from base.method import My_request
from utils.operationExcel import OperationExcel,ExcelMappingYaml
from utils.operationYaml import OperationYaml

excelData = OperationExcel(filename="data.xls",sheet="order").get_data()
# yamlData  = OperationYaml(filename="data.yaml").readYamlDict()

class TestOrder(object):
    @pytest.mark.parametrize(
        "data",excelData
    )
    def test_order(self,data,repair_shopToken,supplierToken):
        caseId = data[OperationExcel.caseId]
        url = data[OperationExcel.caseUrl]
        method = data[OperationExcel.caseMethod]
        # 判断取买家token还是卖家token
        if data[OperationExcel.caseOperator] == "repair_shopToken":
            headers = {"Authorization": repair_shopToken}
        elif data[OperationExcel.caseOperator] == "supplierToken":
            headers = {"Authorization": supplierToken}
        jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(data[OperationExcel.caseParameter])
        expect = data[OperationExcel.caseExpect]

        if caseId == "case014" and method == "GET":
            # jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(data[OperationExcel.caseId])
            res = My_request().GET(url=url, headers=headers, params=jsonData)
            result = res.text

        if method == "GET":
            res = My_request().GET(url=url,headers=headers,params=jsonData)
            result = res.text

        elif method == "POST":
            if caseId == "case024":
                orderId = OperationYaml(filename="public.yaml").readYamlDict()["orderId"]
                url = url + "{0}".format(orderId)    # 将case024拼接上orderId
            res = My_request().POST(url=url,headers=headers,json=jsonData)
            result = res.text
            # 更新case018生成订单参数
            if caseId == "case017":
                modify_content = OperationYaml(filename="data.yaml").readYamlDict()
                addressId = res.json()["data"]["orgDeliveryDTOS"][0]["id"]
                orgId = res.json()["data"]["orgDeliveryDTOS"][0]["orgId"]
                partsList = modify_content["case016"]["partList"]
                modify_content["case018"]["id"] = addressId
                modify_content["case018"]["params"][0]["orgId"] = orgId
                modify_content["case018"]["params"][0]["parts"] = partsList
                OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_content)
            elif caseId == "case018":
                # 更新case019获取支付信息参数
                modify_data = OperationYaml(filename="data.yaml").readYamlDict()
                idList = res.json()["data"]["idList"]
                modify_data["case019"]["idList"] = idList
                modify_data["case023"]["orderId"] = idList[0]
                OperationYaml(filename="data.yaml").updateYaml(modifyItem = modify_data)
                # 更新最新订单id到public.yaml
                modify_public = OperationYaml(filename="public.yaml").readYamlDict()
                modify_public["orderId"] = idList[0]
                OperationYaml(filename="public.yaml").updateYaml(modifyItem = modify_public)

            elif caseId == "case019":
                # 更新case022支付参数
                modify_content = OperationYaml(filename="data.yaml").readYamlDict()
                ids = OperationYaml(filename="data.yaml").readYamlDict()["case019"]["idList"]
                case019_result = res.json()
                payMoney = str(case019_result["data"]["list"][0]["transportFee"] + case019_result["data"]["list"][0]["subTotal"])
                if case019_result["data"]["accountPay"] == 2:
                    payType = 5   # 平台挂账
                elif case019_result["data"]["accountPay"] == 1:
                    payType = 3   # 普通挂账
                modify_content["case022"]["ids"] = ids
                modify_content["case022"]["payMoney"] = payMoney
                modify_content["case022"]["payType"] = payType
                getUrl_prefix = url.split(".")[0]
                returnUrl = modify_content["case022"]["returnUrl"]
                new_returnUrl = returnUrl.replace(returnUrl.split(".")[0],getUrl_prefix)
                modify_content["case022"]["returnUrl"] = new_returnUrl   # 替换returnUrl前缀：url同步caseUrl替换成测试环境还是正式环境
                OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_content)

        # 对所有用例进行断言
        assert expect in result

if __name__ == '__main__':
    pytest.main(["-v","-s","test_3_order.py"])

