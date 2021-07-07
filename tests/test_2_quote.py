#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import pytest
import json
from base.method import My_request
from utils.operationSQL import get_connSql
from utils.operationYaml import OperationYaml
from utils.operationExcel import OperationExcel,ExcelMappingYaml

class TestQuote(object):
    # @property
    # def get_quoteMainId(self):
    #     # 查询到询价单对应的报价单id
    #     newInquiryId = OperationYaml("data", "public.yaml").readYamlDict()["inquiryId"]
    #     sql = "select *from quote_main where inquiry_id = {0};".format(newInquiryId)
    #     selectResult = get_connSql(sql)
    #     newQuoteMainId = str(selectResult[0]["id"])
    #     # 修改yaml文件报价单字典内的id内的参数
    #     OperationYaml.updateYaml(modifyKey="case010",modifyStem=newQuoteMainId)
    excelData = OperationExcel(filename="data.xls",sheet="quote",).get_data()
    yamlData = OperationYaml(filename="data.yaml").readYamlDict()

    @pytest.mark.parametrize(
        "data",excelData
    )
    def test_quote(self,supplierToken,data):
        caseId = data[OperationExcel.caseId]
        url = data[OperationExcel.caseUrl]
        method = data[OperationExcel.caseMethod]
        jsonData = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(data[OperationExcel.caseParameter])
        headers = {"Authorization": supplierToken}
        expect = data[OperationExcel.caseExpect]

        if data[OperationExcel.caseId] == "case011":
            res = My_request().GET(
                url = url,
                params = jsonData,
                headers = headers
            )
            result = res.json()
            # 配件1ID
            partId_01 = result["data"]["quoteDetailList"][0]["partId"]
            originalPriceId_01 = result["data"]["quoteDetailList"][0]["originalPriceId"]
            brandPriceId_01 = result["data"]["quoteDetailList"][0]["brandPriceList"][0]["id"]
            # 配件2ID
            partId_02 = result["data"]["quoteDetailList"][1]["partId"]
            originalPriceId_02 = result["data"]["quoteDetailList"][1]["originalPriceId"]
            brandPriceId_02 = result["data"]["quoteDetailList"][1]["brandPriceList"][0]["id"]
            #主ID
            inquiryId = OperationYaml(filename="public.yaml").readYamlDict()["inquiryId"]
            quoteMainId = OperationYaml(filename="public.yaml").readYamlDict()["quoteMainId"]

            modify_content = OperationYaml(filename="data.yaml").readYamlDict()
            # print(modify_content,type(modify_content))
            modify_content["case012"]["inquiryId"] = inquiryId
            modify_content["case012"]["quoteMainSaveParam"]["id"] = quoteMainId
            modify_content["case012"]["quoteDetailParamList"][0]["partId"] = partId_01
            modify_content["case012"]["quoteDetailParamList"][0]["originalPriceId"] = originalPriceId_01
            modify_content["case012"]["quoteDetailParamList"][0]["brandPriceList"][0]["id"]=brandPriceId_01

            modify_content["case012"]["quoteDetailParamList"][1]["partId"] = partId_02
            modify_content["case012"]["quoteDetailParamList"][1]["originalPriceId"] = originalPriceId_02
            # old_brandPriceId_02 = modify_content["quoteDetailParamList"][1]["brandPriceList"][0]["id"]
            modify_content["case012"]["quoteDetailParamList"][1]["brandPriceList"][0]["id"] = brandPriceId_02
            # 更新yaml中case012的参数
            OperationYaml(filename="data.yaml").updateYaml(modifyItem=modify_content)

        elif method == "GET" and data[OperationExcel.caseId] == "caseA2":
            res = My_request().GET(url=url,headers=headers,params=jsonData)
            # 保存最新报价机构和用户id到public.yaml
            supplierOrgId = res.json()["data"]["orgId"]
            supplierUserId = res.json()["data"]["id"]
            modify_content = OperationYaml(filename="public.yaml").readYamlDict()
            modify_content["supplierOrgId"] = supplierOrgId
            modify_content["supplierUserId"] = supplierUserId
            OperationYaml(filename="public.yaml").updateYaml( modifyItem=modify_content )

        elif  caseId == "case013" and method == "POST":
            res = My_request().POST(
                url=url,
                headers=headers,
                json=jsonData
            )

            # 更新yaml中case015/016的参数
            quote_main_id = OperationYaml(filename="public.yaml").readYamlDict()["quoteMainId"]
            select_result = get_connSql("select *from quote_detail where quote_main_id = {0}".format(quote_main_id))
            idList = list()
            for i in range(len(select_result)):
                id = str(select_result[i]["id"])
                idList.append(id)
            new_content = OperationYaml(filename="data.yaml").readYamlDict()
            new_content["case015"]["quoteDetailIdList"] = idList
            new_content["case016"]["idList"] = idList
            for idx, item in enumerate(idList):
                new_content["case016"]["partList"][idx]["id"] = item
            write_data = OperationYaml(filename="data.yaml").updateYaml(modifyItem=dict(new_content))

        elif method == "POST":
            res = My_request().POST(
                url=url,
                headers=headers,
                json=jsonData
            )
        elif method == "GET":
            res = My_request().GET(
                url=url,
                headers=headers,
                params = jsonData
            )
        assert res.status_code == 200
        assert expect in res.text

if __name__ == '__main__':
    pytest.main(["-v","-s","test_quote.py"])