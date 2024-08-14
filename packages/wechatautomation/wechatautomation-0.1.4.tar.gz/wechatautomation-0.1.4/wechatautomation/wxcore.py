#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@ProjectName: 
@Author: 
@Date: 2024/8/14-下午3:42
@Description: 
-----------------------------------------
"""
from wxelements import wxMainBase
import uiautomation as uia
from wxutils import *


class openWechat(wxMainBase):
    VERSION: str = "__version__"
    lastmsgid: str = None
    listen: dict = dict()
    SessionItemList: list = []
    UiaAPI: uia.WindowControl = uia.WindowControl(ClassName='WeChatMainWndForPC', searchDepth=1) \
 \
        # 功能1：语言版本可切换功能待开发

    # 实例化微信UI
    def __init__(self, isDebug: bool = False, setGlobaltime: int | str = None) -> None:
        openWechat.__switchisDebug(isDebug)
        # 弹出微信窗体
        self._show(HWND=self.UiaAPI)

    @staticmethod
    def __switchisDebug(isDebug: bool) -> None:
        if isDebug:
            wxChatLog.setLevel(10)
            wxChatLog.debug("开启debug")
        else:
            wxChatLog.setLevel(20)
            wxChatLog.info("关闭debug")


if __name__ == '__main__':
    wx = openWechat()
