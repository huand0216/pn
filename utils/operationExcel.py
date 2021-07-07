#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import xlrd
from common.getpath import Public_path
from utils.operationYaml import OperationYaml

class OperationExcel(object):
    caseId = "caseID"
    caseRemarks = "描述"
    caseOperator = "操作方（修理厂/供应商）"
    caseMethod = "请求方法"
    caseUrl = "请求地址"
    caseParameter = "请求参数"
    caseExpect = "预期结果"

    def __init__(self,dirname = "data",filename = "data.xls",sheet = None):
        '''
        :param dirname: 指定目录
        :param filename: 指定文件
        :param sheet: 指定sheet
        '''
        self.dirname = dirname
        self.filename = filename
        self.sheet = sheet

    # 获取sheet
    def get_sheet(self):
        book = xlrd.open_workbook(filename=Public_path().get_path(self.dirname,self.filename))
        sheet = book.sheet_by_name(self.sheet)
        return sheet

    # 获取有效行数
    def valid_rows(self):
        return self.get_sheet().nrows

    # 获取有效列数
    def valid_cols(self):
        return self.get_sheet().ncols

    # 获取指定行指定列的值
    def getValue(self,row,col):
        value = self.get_sheet().cell_value(row,col)
        return value

    # 获取Excel内的数据
    def get_data(self):
        data = list()
        key =  self.get_sheet().row_values(0)
        for i in range(1,(self.valid_rows())):
            col_value = self.get_sheet().row_values(i)
            item = dict(zip(key,col_value))
            data.append(item)
        return data
'''
映射Excel和yaml的请求数据
'''
class ExcelMappingYaml():
    def __init__(self,dirname = "data",filename = None):
        self.dirname = dirname
        self.filename = filename

    def get_mappingYaml(self,key):
        if key != '':
            yamlData = OperationYaml(self.dirname,self.filename).readYamlDict()
            return yamlData[key]
        elif key == '':
            return None
        # yamlData = OperationYaml(self.dirname, self.filename).readYamlDict()
        # return yamlData

if __name__ == '__main__':
    # item = ExcelMappingYaml(filename="data.yaml").get_mappingYaml(key="case017")
    # print(item)
    # excelData = OperationExcel(filename="data.xls",tableName="parse").get_data()
    # # print(type(MappingYaml("data","inquiry.yaml").get_mappingYaml(excelData["请求参数"])))
    # for item in excelData:
    #     print(item[OperationExcel.caseRemarks])
    data = OperationExcel(dirname="data",filename="data.xls",sheet="parse").get_data()
    print(data)