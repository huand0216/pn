#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong


import pytest
import pytest_html
import allure
import os
from common.getpath import Public_path

if __name__ == '__main__':
    # pytest.main(["-v","-s", "./tests/"])
    pytest.main(["-v","-s","./tests/","--alluredir","{0}/result".format(Public_path().get_path(dirname="report",filename=""))])
    import subprocess
    os.environ["PATH"] += os.pathsep + '/Users/administrator/.allure-2.7.0/bin'
    subprocess.call('allure generate {0}/result/ -o {1}/html --clean'.format(Public_path().get_path(dirname="report",filename=""),Public_path().get_path(dirname="report",filename="")),shell=True)
    # subprocess.call('allure open -h 127.0.0.1 -p 8088 {0}/html'.format(Public_path().get_path(dirname="report",filename="")),shell=True)