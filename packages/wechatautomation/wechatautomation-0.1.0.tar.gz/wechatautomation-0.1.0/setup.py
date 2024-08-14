#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@ProjectName: 
@Author: 
@Date: 2024/8/12-下午3:44
@Description: 
-----------------------------------------
"""

import codecs
import os

from setuptools import find_packages, setup

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


# 读取 requirements.txt 文件
def read_requirements():
    with open('requirements.txt', 'r') as req_file:
        return req_file.read().splitlines()


# 从 requirements.txt 文件中获取依赖项
install_requires = read_requirements()

VERSION = '0.1.0'
DESCRIPTION = '微信自动化程序'
LONG_DESCRIPTION = 'None'

# 使用setuptools的setup函数来配置和安装Python包
setup(
    # 包的名称
    name="wechatautomation",
    # 包的版本号，使用预定义的VERSION变量
    version=VERSION,
    # 作者姓名
    author="Anthony Lee",
    # 作者电子邮件，此处为空字符串
    author_email="1020343877@qq.com",
    # 包的简短描述
    description=DESCRIPTION,
    # 长描述的内容类型，此处指定为markdown格式
    long_description_content_type="text/markdown",
    # 长描述的文本，通常包含包的详细信息和使用说明
    long_description=long_description,
    # 自动发现和包含所有Python包
    packages=find_packages(),
    package_data={
        'wechatautomation': ['requirements.txt']
    },
    # 定义包的依赖关系，根据不同的操作系统选择不同的getch库
    install_requires=install_requires,
    # 关键词列表，用于在包仓库中帮助用户搜索
    keywords=['python', 'uiautomation', 'toml', 'wechat'],
    # 包的分类信息，用于在包仓库中对包进行分类
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix"
    ]
)
