#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-07-16 22:17:09
LastEditTime: 2021-07-17 22:40:53
Description: `logurn` 日志模块的学习测试
"""
import sys

from loguru import logger

# 用字典配置 `loguru` 模块
config = {
    # 添加接收器
    "handlers": [
        # 写入日志文件,只需要使用字符串路径作为接收器;为了方便,它自带{time}:
        # compression="zip": 在结束程序时压缩日志文件
        # rotation="500 MB/12:00/1 week": 自动分割超过500MB的文件/每天中午创建新文件/文件超过一星期就会分割
        # retention="10 days": 自动清理超过10天的文件
        {"sink": "file.log", "rotation": "1 day", "encoding": "utf-8"},
        # 配置控制台输出
        # `sys.stdout` 类似 `print` 的输出.(控制台流输出)
        # `sys.stderr` 重定向错误输出.
        # `format` 设置日志输出的格式. "format": "{time} - {message}"
        # backtrace(回溯)=True, diagnose(诊断)=True : 显示堆栈详细错误
        {"sink": sys.stdout, "backtrace": True, "diagnose": True},
        # Json化日志输出,以便更容易地解析或传递它们
        # 使用serialize参数,每个日志消息将在发送到配置接收器之前转换为JSON字符串。
        # {"sink": sys.stdout, "serialize": True},
    ],
}
# 也可以用 `add()` 增加日志接收器.
# 它会自动识别 `sink` 的类型: 简单函数、字符串路径、类文件对象、协程函数或内置处理程序
# logger.add(sink="utf-8",encoding="utf-8")

logger.configure(**config)
logger.debug("我喜欢黄颖怡")
# 堆栈跟踪的用法
# try:
#     t = 0
#     var = 0 / t
# except Exception as e:
#     logger.exception("what?!")

logger.info("黄颖怡喜欢另一个男士")
logger.info("男士: {user}", user="anybody")  # 日志参数传递

# 绑定技术
# logger.add(sys.stdout, format="{extra[ip]} {extra[user]} {message}")
# context_logger = logger.bind(ip="192.168.0.1", user="someone")
# context_logger.info("Contextualize your logger easily")
# context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
# context_logger.info("Use kwargs to add context during formatting: {user}", user="anybody")
