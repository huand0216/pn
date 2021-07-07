#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pytest
from base.method import My_request
from utils.operationExcel import OperationExcel,ExcelMappingYaml
from utils.operationYaml import OperationYaml
from utils.operationSQL import get_connSql

class Test_inquiry(object):

    excelData = OperationExcel(filename="data.xls",sheet="inquiry").get_data()
    # yamlData = OperationYaml(filename="data.yaml").readYamlDict()

    @pytest.mark.parametrize(
        "data",excelData
    )
    def test_inquiry(self,data,repair_shopToken):
        caseId = data[OperationExcel.caseId]
        url = data[OperationExcel.caseUrl]
        method = data[OperationExcel.caseMethod]
        jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(key=data[OperationExcel.caseParameter])
        headers = {"Authorization": repair_shopToken}
        expect = data[OperationExcel.caseExpect]

        if caseId == "case008":
            res = My_request().my_request(url=url,method=method,json=jsonData,headers=headers
                                        )
            inquiryId = res.json()["data"]["records"][0]["id"]
            # 将最新的询价单id和报价单id写入yaml文件
            modify_public = OperationYaml(filename="public.yaml").readYamlDict()
            modify_public["inquiryId"] = str(inquiryId)

            sql = "select *from quote_main where inquiry_id = {0};".format(inquiryId)
            selectResult = get_connSql(sql)
            newQuoteMainId = str(selectResult[0]["id"])
            modify_public["quoteMainId"] = str(newQuoteMainId)
            write_public = OperationYaml("data","public.yaml").updateYaml(modifyItem=dict(modify_public))

            # 更新data.yaml内'case014'的参数case010,case011参数
            modify_data = OperationYaml(dirname="data",filename="data.yaml").readYamlDict()
            modify_data["case014"]["inquiryId"] = inquiryId
            modify_data["case010"]["quoteMasterId"] = newQuoteMainId
            modify_data["case011"]["quoteMainId"] = newQuoteMainId
            write_data = OperationYaml("data","data.yaml").updateYaml(modifyItem=dict(modify_data))

        elif data[OperationExcel.caseMethod] == "GET":
            res = My_request().GET(url=url,headers=headers,params=jsonData)
            repair_shopOrgId = res.json()["data"]["orgId"]
            repair_shopUserId = res.json()["data"]["id"]

            # 更新public内的参数
            modify_public = OperationYaml(dirname="data",filename="public.yaml").readYamlDict()
            modify_public["repair_shopOrgId"] = repair_shopOrgId
            modify_public["repair_shopUserId"] = repair_shopUserId
            write_public = OperationYaml(filename="public.yaml").updateYaml(modifyItem=modify_public)

        elif data[OperationExcel.caseMethod] == "POST":
            res = My_request().POST(url=url,json = jsonData,headers = headers )
            if caseId == "case005":
                # 将询价供应商list更新到case007的参数
                orgIdList = list(map(lambda i:i["orgId"],res.json()["data"]))   # 获取到最新的orgIdList
                modify_data = OperationYaml(filename="data.yaml").readYamlDict()
                modify_data["case007"]["orgIdList"] = orgIdList
                OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_data)   # 更新

        result = res.text
        assert res.status_code == 200
        assert expect in result

if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_1_inquiry.py"])



