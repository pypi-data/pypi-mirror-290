#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@ProjectName: PyServer
@Author: Anthony Lee
@Date: 2024/8/10-下午9:46
@Description: 
-----------------------------------------
"""

from wxlogging import wxChatLog
from wxutils import *
import uiautomation as uia
import datetime
import time
import os
import re
import win32gui


class wxMainBase:
    def _show(self, HWND):
        try:
            self.HWND = wxFindWindow(contronlClass="WeChatMainWndForPC")
            wxChatLog.debug(f"当前用户界面窗口句柄：{self.HWND}")
            win32gui.ShowWindow(self.HWND, 1)
            win32gui.SetWindowPos(self.HWND, -1, 0, 0, 0, 0, 3)
            win32gui.SetWindowPos(self.HWND, -2, 0, 0, 0, 0, 3)
            HWND.SwitchToThisWindow()
        except Exception as e:
            wxChatLog.error(e)

    @property
    def _app_path(self):
        wxChatLog.debug(f"当前用户界面窗口句柄：私有属性待开发")


# 登录窗体
class wechatLoginHandle:
    _uiaClassName = 'WeChatLoginWndForPC'
    wxuiaMainApi = uia.PaneControl(ClassName=_uiaClassName, searchDepth=1)

    def __repr__(self) -> str:
        return f"<wxAutomation.wechatHandle object at {hex(id(self))}>"

    # 前置微信窗口
    def _show(self):
        try:
            # 获取窗口句柄
            self.wxHWND = wxFindWindow(contronlClass="WeChatMainWndForPC")
            wxChatLog.debug(f"当前窗口句柄：{self.wxHWND}")
            # 显示窗口，参数1表示可见
            win32gui.ShowWindow(self.wxHWND, 1)
            win32gui.SetWindowPos(self.wxHWND, -1, 0, 0, 0, 0, 3)
            win32gui.SetWindowPos(self.wxHWND, -2, 0, 0, 0, 0, 3)
            self.wxuiaMainApi.SwitchToThisWindow()
        except Exception as e:
            wxChatLog.error(e)

    # 返回窗口句柄的路径信息
    @property
    def _app_path(self):
        HWND = wxFindWindow(contronlClass="WeChatMainWndForPC")
        wxChatLog.debug(f"当前登录界面窗口句柄：{wxGetPathByHwnd(HWND)}")
        return wxGetPathByHwnd(HWND)

    # 点击进入微信
    def clickLogin(self):
        wxLoginButton = self.wxuiaMainApi.ButtonControl(Name='进入微信')
        # if wxLoginButton.Exists():
        #     wxLoginButton.Click(simulateMove=isMouseTracks)


if __name__ == '__main__':
    wechat_instance = wechatLoginHandle()
    wechat_instance._show()
    wechat_instance.clickLogin()
