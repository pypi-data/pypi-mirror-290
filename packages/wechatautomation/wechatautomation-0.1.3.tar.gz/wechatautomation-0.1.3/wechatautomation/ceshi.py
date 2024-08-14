#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@ProjectName: 
@Author: 
@Date: 2024/8/12-下午3:42
@Description: 
-----------------------------------------
"""
from os import getcwd
from requests import get as reqget
from .wxlogging import wxChatLog


def get():
    print(6666)
    result = getcwd()
    print(result)
    res = reqget("https://www.baidu.com", timeout=3)
    wxChatLog.info("测试信息")
    print(res.status_code)


if __name__ == '__main__':
    get()
