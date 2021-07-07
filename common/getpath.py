#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

import os

class Public_path(object):

    def get_path(self,dirname,filename):
        root = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(root,dirname,filename)

if __name__ == '__main__':
    print(Public_path().get_path(dirname="data",filename=""))