# -*- coding: utf-8 -*-
# @Time : 2021/12/12 2:27
# @Author : WhaleFall
# @Site : 
# @File : setting.py.py
# @Software: PyCharm
# 配置文件
from pathlib import Path
import os

# Email config
EMAIL_USERNAME = "whalefall2020@163.com"
EMAIL_PASSWORD = "BFEPKZGIINCMBEGM"
EMAIL_SMTP_HOST = "smtp.163.com"
EMAIL_SMTP_PORT = 994
EMAIL_SMTP_SSL = True


class BaseConfig:
    """主配置文件"""
    basedir = Path(__file__).resolve().parent  # 项目绝对路径
    dirs = ['db', 'logs', 'markdown']  # 要有的目录
    # 在环境变量中获取邮箱配置
    email_config = {
        "username": os.environ.get('EMAIL_USERNAME') or EMAIL_USERNAME,
        "password": os.environ.get('EMAIL_PASSWORD') or EMAIL_PASSWORD,
        "smtp_host": os.environ.get('EMAIL_SMTP_HOST') or EMAIL_SMTP_HOST,
        "smtp_port": os.environ.get('EMAIL_SMTP_PORT') or EMAIL_SMTP_PORT,
        "smtp_ssl": os.environ.get('EMAIL_SMTP_SSL') or EMAIL_SMTP_SSL
    }
    logs_dir = Path(basedir, "logs")  # 日志存放的文件夹

    def __init__(self):
        """程序初始化"""
        # 若目录不存在新建目录
        for dirs in BaseConfig.dirs:
            Path.mkdir(BaseConfig.basedir, dirs, exist_ok=True)


class TestConfig(BaseConfig):
    """测试配置"""
    pass


configs = {
    "default": BaseConfig,
    "test": TestConfig
}
config = configs[os.environ.get("CONFIG") or "default"]  # 从环境变量中获取配置类型
