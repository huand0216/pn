#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

from common.getpath import Public_path
from utils.operationYaml import OperationYaml
from utils.operationExcel import OperationExcel


# dict1 = {"data":{"quoteDetailList":[{"image":"l9XABYsI7gNhJEEksNH1t4U15AfH0urC8CO7+qi28c0=","originalPrice":0.01,"partId":"1410045188177117186","count":1,"inquiryRemark":"","originalPriceId":"1410045193042509826","ifHaveOem":True,"imagePrePath":"Bmw","partName":"前大灯总成（右）","referencePrice":6510.00,"appendFlag":0,"oem":"63127177730","carPriceList":[],"brandPriceList":[{}]},{"image":"l9XABYsI7gNhJEEksNH1t4U15AfH0urC8CO7+qi28c0=","referencePrice":6510.00,"appendFlag":0,"partId":"1410045188185505794","oem":"63127177729","count":1,"inquiryRemark":"","carPriceList":[],"ifHaveOem":True,"imagePrePath":"Bmw","partName":"前大灯总成（左）","brandPriceList":[{}]}],"quoteMain":{"quoted":0,"code":"BJ2106300009267018","orgName":"自动化供应商","inquiryType":10,"transportFee":0.00,"showBrandCode":0,"quoteEmpId":"28593","quoteEmpName":"自动化","firstQuoteEmpId":"28593","id":"1410045188248420353","status":10,"createDate":"2021-06-30 09:19:05"},"inquiryMain":{"code":"XJ2106300003444607","createOrderStatus":0,"endDate":"2021-07-01 09:19:05","requireOEM":0,"remark":"","source":2,"quoted":0,"cityName":"花地玛堂区","optionCode":"000","modelInquiry":False,"vin":"WBAPX32060C186115","carInfo":"进口宝马 5 Series/5系 2.0T 6AT","id":"1410045188160339970","mjsid":False,"images":[],"districtName":"花地玛堂区","inquiryOrgId":"19480","inquiryOrgName":"修理厂aa","maker":"进口宝马","plateNum":"","imagePrePath":"Bmw","quality":"0,1","totalAmount":2,"inquiryEmpName":"a","inquiryEmpPhone":"20000000000","vinType":1,"detailAddress":"文辉建筑工程","invoice":2,"provinceName":"澳门特别行政区","quoteTotal":1,"startDate":"2021-06-30 09:19:05","status":30}},"errCode":0,"msg":None}
#
# brandPriceId_01 = dict1["data"]["quoteDetailList"][0]["brandPriceList"][0]["id"]
# print(brandPriceId_01)