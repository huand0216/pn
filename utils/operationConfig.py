#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:Huandong

from common.getpath import Public_path
import configparser

def get_configparser(label):
    config = configparser.ConfigParser()
    config.read(Public_path().get_path("config","configparser.ini"))
    return dict(config.items(label))

