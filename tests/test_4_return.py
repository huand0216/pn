#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pytest
import string
from base.method import My_request
from utils.operationExcel import OperationExcel,ExcelMappingYaml
from utils.operationYaml import OperationYaml

class Test_return(object):
    excelData = OperationExcel(filename="data.xls",sheet="order_return").get_data()

    @pytest.mark.parametrize(
        "data",excelData
    )
    def test_return(self,data,repair_shopToken,supplierToken):
        caseId = data[OperationExcel.caseId]
        url = data[OperationExcel.caseUrl]
        method = data[OperationExcel.caseMethod]
        remark = data[OperationExcel.caseRemarks]
        operator = data[OperationExcel.caseOperator]
        parameter = data[OperationExcel.caseParameter]      #参数
        expect = data[OperationExcel.caseExpect]

        if operator == "repair_shopToken":
            headers = {"Authorization": repair_shopToken}
        elif operator == "supplierToken":
            headers = {"Authorization": supplierToken}
        jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(parameter)

        # 发送请求
        if (caseId == "case030" or caseId == "case032") and method == "GET":
            # 将case030拼接上returnId
            returnId = OperationYaml(filename="public.yaml").readYamlDict()["returnId"]
            url = url + "{0}".format(returnId)
            res = My_request().GET(url=url, headers=headers, params=jsonData)
            result = res.text

        elif method == "GET":
            if caseId == "case025":
                orderId = OperationYaml(filename="public.yaml").readYamlDict()["orderId"]
                url = url + "{0}".format(orderId)  # 将case025url拼接上orderId
            res = My_request().GET(url=url , headers=headers , params = jsonData)
            result = res.text
            # 更新case025申请退货参数
            if caseId == "case025":
                orderReturnDetailDTO = list()
                l = res.json()["data"]["orderDetailVOS"]
                for i in range(len(l)-1):
                    orderReturnDetail = {"orderDetailId": "", "returnCount": 1, "backMoney": 200, "degreeVersion": 1}
                    orderReturnDetail["orderDetailId"] = l[i]["id"]
                    orderReturnDetail["returnCount"] = l[i]["partCount"]
                    orderReturnDetail["backMoney"] = l[i]["subtotal"]
                    orderReturnDetailDTO.append(orderReturnDetail)
                modify_data = OperationYaml(filename="data.yaml").readYamlDict()
                modify_data["case026"]["orderReturnDetailDTO"] = orderReturnDetailDTO  # 更新子订单orderReturnDetailDTO
                modify_data["case026"]["orderId"] = res.json()["data"]["orderMainVO"]["id"]  # 更新主订单id
                modify_data["case026"]["returnAmount"] = res.json()["data"]["orderMainVO"]["finalPrice"]  # 更新退货总金额
                OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_data)

        elif method == "POST":
            res = My_request().POST(url=url,headers=headers,json=jsonData)
            result = res.text
            '''1.拿到退货单id更新到public.yaml
            '''
            if caseId == "case026":
                returnId = res.json()["data"]
                modify_public = OperationYaml(filename="public.yaml").readYamlDict()
                modify_public["returnId"] = returnId     # 替换掉旧退货单id
                OperationYaml(filename="public.yaml").updateYaml(modify_public)  # 更新

            # 更新case028退货审核参数,case029退货单发货id
            elif caseId == "case027":
                modify_data = OperationYaml(filename="data.yaml").readYamlDict()
                return_deliveryId = res.json()["data"]["orgDeliveryDTOS"][0]["id"]
                modify_data["case028"]["deliveryId"] = return_deliveryId    # 替换收货地址id
                returnId = OperationYaml(filename="public.yaml").readYamlDict()["returnId"]
                modify_data["case028"]["id"] = returnId# 替换掉旧退货单id
                modify_data["case029"]["orderId"] = returnId
                OperationYaml(filename="data.yaml").updateYaml(modify_data)   # 更新

        # 对所有用例进行断言
        assert expect in result

if __name__ == '__main__':
    pytest.main(["-v","-s","test_return.py"])





