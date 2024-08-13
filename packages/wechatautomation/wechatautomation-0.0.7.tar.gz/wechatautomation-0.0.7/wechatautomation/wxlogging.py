#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@ProjectName: 
@Author: 
@Date: 2024/8/10-上午11:25
@Description: 
-----------------------------------------
"""

import logging
from colorama import Fore, Style
import colorama


# 初始化 colorama
colorama.init(autoreset=True)
objName = "wechatautomation"


class ColorFormatter(logging.Formatter):
    def format(self, record):
        colors = {
            logging.DEBUG: Fore.LIGHTBLACK_EX,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.RED + Style.BRIGHT,
        }
        color = colors.get(record.levelno, Fore.WHITE)
        log_format = (
            f'{color}[%(levelname)s]{Style.RESET_ALL} '
            f'{Fore.LIGHTBLACK_EX}%(asctime)s{Style.RESET_ALL} '
            f'{Fore.LIGHTBLACK_EX}%(logger_name)s{Style.RESET_ALL} '
            f'({Fore.CYAN}%(filename)s{Style.RESET_ALL}:{Fore.CYAN}%(lineno)d{Style.RESET_ALL}): '
            f'{color}%(message)s{Style.RESET_ALL}'
        )
        if not hasattr(record, 'logger_name'):
            record.logger_name = objName

        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class wxAutomationLogger:
    def __init__(self, loggerName: str = objName):
        self.wxAutomation = logging.getLogger(loggerName)
        self.wxAutomation.setLevel(logging.DEBUG)
        self.wxAutomationLoggerHandle = logging.StreamHandler()
        self.wxAutomationLoggerHandle.setLevel(logging.DEBUG)
        self.wxAutomationLoggerFormater = ColorFormatter()
        self.wxAutomationLoggerHandle.setFormatter(self.wxAutomationLoggerFormater)
        self.wxAutomation.addHandler(self.wxAutomationLoggerHandle)
        self.wxAutomation.propagate = False


wxChatLog = wxAutomationLogger().wxAutomation
# result = read_toml()
# if result['debug']['isDeBug']:
#     wxChatLog.info("设置当前Debug级别")
#     wxChatLog.setLevel(10)
# else:
#     wxChatLog.setLevel(20)


