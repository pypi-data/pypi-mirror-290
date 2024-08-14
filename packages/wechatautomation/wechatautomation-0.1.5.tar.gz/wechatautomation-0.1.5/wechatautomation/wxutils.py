# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@ProjectName:
@Author:
@Date: 2024/8/10-下午5:11
@Description: 
-----------------------------------------
"""
from .wxlogging import wxChatLog
from win32gui import FindWindow
from win32process import GetWindowThreadProcessId
from psutil import Process
from typing import Dict, Union, Type
import uiautomation as uia

# 支持版本
VERSION = "3.9.11.17"

uia.SetGlobalSearchTimeout(0)


def ceshi1():
    wxChatLog.debug(1111111111111111)
    wxChatLog.error("123")


def wxFindWindow(contronlClass: str = None, controlName: str = None, ):
    """
    通过窗口类名或者窗口标题查找窗口句柄
    """
    try:
        wxChatLog.debug("查找窗口句柄", extra={'logger_name': 'FindWindow()'})
        return FindWindow(contronlClass, controlName)
    except Exception as e:
        wxChatLog.critical(e, extra={'logger_name': '111'})


# 通过HWND获取窗口路径信息
def wxGetPathByHwnd(hwnd):
    """
    通过窗口句柄获取窗口路径信息
    """
    try:
        threading_id, process_id = GetWindowThreadProcessId(hwnd)
        process = Process(process_id)
        return process.exe()
    except Exception as e:
        wxChatLog.critical(e, extra={'logger_name': 'GetPathByHwnd()'})
        return None
