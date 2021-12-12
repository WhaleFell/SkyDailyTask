# -*- coding: utf-8 -*-
# @Time : 2021/12/12 11:05
# @Author : WhaleFall
# @Site : 
# @File : log.py
# @Software: PyCharm
# 日志模块
import sys
from loguru import logger
from setting import config

# 用字典配置 `loguru` 模块
config = {
    # 添加接收器
    "handlers": [
        # 写入日志文件不必用颜色,rotation="1 day": 文件超过一天就会分割
        # run_{time:YYYY_M_D}.log: 日志格式
        {"sink": str(config.logs_dir) + "/run_{time:YYYY_M_D}.log", "rotation": "1 day", "encoding": "utf-8",
         "backtrace": True, "diagnose": True, "colorize": False},
        # 标准输出流
        {"sink": sys.stdout, "backtrace": True, "diagnose": True, "colorize": True},
    ],
}
logger.configure(**config)
