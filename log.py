#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-07-16 22:17:09
LastEditTime: 2021-07-17 22:40:53
Description: 日志文件
'''
import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志关系映射

    def __init__(self, filename, level='info', backCount=10, fmt='%(asctime)s - %(pathname)s [line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别

        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        self.logger.addHandler(sh)  # 把对象加到logger里

        fh = handlers.RotatingFileHandler(
            filename=filename, maxBytes=10485760, backupCount=backCount)   # 按照文件大小分割日志文件
        fh.setLevel(self.level_relations.get(level))
        fh.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(fh)

log = Logger('run.log', level='debug')
if __name__ == '__main__':
    log = Logger('run.log', level='debug')
    log.logger.debug('详细信息，调试使用')
    log.logger.info('正常信息')
    log.logger.warning('警告信息')
    log.logger.error('错误信息')
    log.logger.critical('问题很严重')
