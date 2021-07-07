#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import yaml
from common.getpath import Public_path

class OperationYaml(object):

    def __init__(self,dirname="data",filename=None):
        '''
        :param dirname: 指定yaml文件目录
        :param filename: 指定yaml文件名称
        '''
        self.dirname = dirname
        self.filename = filename

    # 获取yaml内的数据，返回列表数据
    def readYamlList(self):
        with open(Public_path().get_path(dirname=self.dirname,filename=self.filename)) as f:
            return list(yaml.safe_load_all(f))

    # 获取yaml内的数据，返回字典数据
    def readYamlDict(self):
        with open(Public_path().get_path(dirname=self.dirname,filename=self.filename)) as af:
            result = yaml.safe_load(af)
            return result

    # def writeYaml(self,data):
    #     yaml.safe_load(data)

    # 修改yaml文件
    def  updateYaml(self,modifyItem):
        # with open(Public_path().get_path(self.dirname,self.filename)) as f:
        #     content = yaml.load(stream=f,Loader=yaml.FullLoader)
        #     if modifyKey == None:
        #         content[modifyCase] = modifyItem
        #     elif modifyCase == None:
        #         content[modifyKey] = modifyItem
        #     else:
        #         content[modifyCase][modifyKey] = modifyItem
        #     data = content
        # with open(Public_path().get_path(self.dirname,self.filename),"w") as nf:
        #     yaml.safe_dump(data=modifyItem,stream=nf,encoding="utf-8",allow_unicode=True)
        data = modifyItem
        with open(Public_path().get_path(dirname=self.dirname,filename=self.filename), "w") as f:
            yaml.dump(data=data,stream=f,encoding = "utf-8",allow_unicode = True)

    # 普通文本写入
    def writeTxt(self,content):
        with open(Public_path().get_path(dirname=self.dirname,filename=self.filename),"w") as f:
            f.write(content)

    # 普通文本读取
    def readTxt(self):
        with open(Public_path().get_path(dirname=self.dirname,filename=self.filename),"r") as f:
            return f.read()


if __name__ == '__main__':
    # modifyStem = {"quoteMasterId":"123"}
    # OperationYaml("data","data.yaml").updateYaml(modifyKey="case010",modifyStem=modifyStem)
    # item = OperationYaml(filename="public.yaml").readYamlDict()["quoteMainId"]
    # OperationYaml(filename="data.yaml").updateYaml(modifyCase="case014",modifyKey="inquiryId",modifyItem="1403188029082169345")
    OperationYaml(filename="data.yaml").updateYaml(modifyItem="1122")