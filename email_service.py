#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-07-16 22:12:17
LastEditTime: 2021-07-22 01:20:19
Description: 邮件发送模块
'''
from logging import log
import zmail
import configparser
from log import log
import os
import time


def writeConfig():
    cf = configparser.ConfigParser()
    if os.path.exists("config.ini"):
        os.remove("config.ini")
        print("删除")

    cf.add_section("email")
    cf.set("email", "username", "邮箱账号")
    cf.set("email", "password", "邮箱密码")
    cf.set("email", "smtp_host", "收件服务器地址")
    cf.set("email", "smtp_port", "收件服务器端口")
    cf.set("email", "smtp_ssl", "收件是否加密")
    # cf.set("email", "smtp_tls", "收件tls")
    cf.add_section("sendTo")
    cf.set("sendTo", "address", "需要发送的邮件地址")
    cf.write(open("config.ini", "w", encoding="utf8"))


class EmailService(object):
    def __init__(self) -> None:
        '''初始化方法,读取配置文件'''
        try:
            cf = configparser.ConfigParser()
            cf.read("config.ini", encoding="utf-8")
            self.username = cf.get("email", "username")  # 用户名
            self.password = cf.get("email", "password")
            self.smtp_host = cf.get("email", "smtp_host")
            self.smtp_port = cf.get("email", "smtp_port")
            self.smtp_ssl = cf.get("email", "smtp_ssl")
            # self.smtp_tls = cf.get("email", "smtp_tls")
            self.sendTo = cf.get("sendTo", "address")  # 支持多邮箱
            # self.service = None
        except Exception as e:
            log.logger.warning("读取配置文件时出现问题!请重新修改")
            writeConfig()

    def serviceStatus(self):
        '''检查邮件服务可用性'''
        self.service = zmail.server(
            username=self.username,
            password=self.password,
            smtp_host=self.smtp_host,
            smtp_port=self.smtp_port,
            smtp_ssl=self.smtp_ssl,
            # smtp_tls=self.smtp_tls,
        )
        if self.service.smtp_able():
            # log.logger.info("邮箱配置正确")
            return True
        else:
            log.logger.warning("邮箱配置异常")
            return False

    def sendEmail(self, sendTo, html, fileList=[]):
        '''传入接收的邮箱,发送html文件与markdown附件和日志文件'''

        # 判断状态
        if not self.serviceStatus():
            return

        mail = {
            'subject': "光遇|%s每日任务" % (time.strftime("%Y年%m月%d日")),
            'content_html': html,
            'attachments': fileList,
        }
        try:
            status = self.service.send_mail(sendTo, mail)

            if status:
                log.logger.info(f"{sendTo}邮件推送成功!")
            else:
                log.logger.warning(f"{sendTo}邮件推送失败!")
        except Exception as e:
            log.logger.warning(f"{sendTo}发信未知失败: {e}")


    def send_emails(self, html, fileList=[]):
        '''处理多个邮箱'''
        email_list = self.sendTo.split(",")
        for emailID in email_list:
            self.sendEmail(emailID, html, fileList)
            time.sleep(5)


if __name__ == "__main__":
    mail = EmailService()
    # mail.serviceStatus()
    mail.sendEmail("<h1>黄颖怡去那所高中了</h1>")
