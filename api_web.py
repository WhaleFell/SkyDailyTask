#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-07-15 22:17:41
LastEditTime: 2021-07-22 17:27:31
Description: 网易大神-光遇每日任务爬虫
'''
from log import log
import requests
from lxml import etree
import re
import html2text  # html 转 md
# from email_service import EmailService
import os
import time
import random


class SkyTask(object):
    '''获取光遇任务类'''

    def __init__(self) -> None:
        '''初始化方法,用手机UA请求'''
        self.header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36",
        }
        # 光遇小管家主页
        self.index_url = "https://m.ds.163.com/user/95c6340497c7415c9970f94ec14625c6"
        # self.log = Logger('run.log', level='debug')  # 日志记录器

    def getIndex(self) -> list:
        '''获取文章链接,返回一个 (标题,链接) 的元组组成的列表'''

        try:
            resp = requests.get(self.index_url, headers=self.header).text
            # print(resp)
            html = etree.HTML(resp)
            urlList = html.xpath(
                r"//div[@class='feed-card']//div[@class='feed-brief-card']/a/@href")
            # 直接匹配出网址了,草!
            urls = [
                f"https://m.ds.163.com{url}"
                for url in urlList
            ]

        except Exception as e:
            log.logger.warning(f"解析文章链接错误! {e}")
            return False
        return urls

    def parse(self, article_url) -> list:
        '''获取文章详细,返回提取后的HTML和标题'''
        try:
            resp = requests.get(article_url, headers=self.header).text
            pat = re.compile(
                r'<article class="feed-article__content">(.*?)</article>')
            pat_title = re.compile(
                r'<h1 class="feed-article__headline mb-l">(.*?)</h1>')
            html = pat.findall(resp)[0]
            title = pat_title.findall(resp)[0]
        except Exception as e:
            log.logger.warning(f"{article_url}解析失败! {e}")
            return False, False

        return title, html

    def disposeHTML(self, html: str):
        '''处理HTML去除头部广告,添加自适应宽度.'''
        # 广告中的链接会变的,弃用,改用正则
        # AD = '<p align="center"><a href="https://app.16163.com/ds/ulinks/?utm_term=wyds_dl_kf_gy_xy_5cb546a0d5456870b97d9424"><img src="https://ok.166.net/reunionpub/ds/kol/20210718/005226-vq0bdpwgsu.png" width="100%" height="100%"></a></p>'

        # 高宽自适应,匹配所有,异常处理
        try:
            html = html.replace("<p><br></p>", "")  # 替换掉分割线
            # 去除广告,可能误杀,我的垃圾正则技术.
            html = re.sub(r"<p[\S\s]+</a></p>", "", html)
            html = re.sub(r'width="[0-9]*"', 'width="100%"', html)
            html = re.sub(r'height="[0-9]*"', 'height="100%"', html)

        except Exception as e:
            log.logger.warning(f"文章净化失败! {e}")

        return html

    def makedir(self):
        '''新建目录'''
        if not os.path.exists("markdown"):
            os.mkdir("markdown")
        if not os.path.exists("html"):
            os.mkdir("html")

    def __getTitle(self, md: str) -> str:
        '''弃用:获取md文件的第一行'''
        return md.splitlines()[0]

    def checkNameValid(self, name=None):
        '''文件夹符合规范'''
        if name is None:
            print("name is None!")
            return
        reg = re.compile(r'[\\/:*?"<>|\r\n]+')
        valid_name = reg.findall(name)
        if valid_name:
            for nv in valid_name:
                name = name.replace(nv, "_")
        return name

    def docs_exist(self, file_name):
        '''TODO: 文件重名自适应,递归,'''
        if os.path.exists(os.path.join("html", "%s.html" % (file_name))):
            pass

    def writeDoc(self, md: str, html: str, title: str):
        '''写文件 传入md,html字符串和标题,返回md文件的位置和处理后html内容'''
        MDheader = '''---
title: %s
date: %s
categories: Sky光•遇
tags: [Sky光•遇,%s]
description: 
index_img: https://ok.166.net/reunionpub/ds/kol/20210722/001554-k2u90bj7ay.png?imageView&thumbnail=600x0&type=jpg
banner_img: https://ok.166.net/reunionpub/ds/kol/20210722/001554-k2u90bj7ay.png?imageView&thumbnail=600x0&type=jpg
---''' % (title, time.strftime("%Y-%m-%d %H:%M:%S"), title)

        # 构造文件名
        strtime = time.strftime("%Y-%m-%d")
        file_name = "%s %s" % (strtime, self.checkNameValid(title))
        md = f"{MDheader}\n# {title}\n{md}"  # 为md文件加标题和博客头
        html = f"<h1>{title}</h1>{html}"  # 为 html 添加标题

        # 重名处理
        if os.path.exists(os.path.join("html", "%s.html" % (file_name))):
            file_name = "%s[%s]" % (file_name, random.randint(0, 9999))

        # 写文件
        self.makedir()  # 建目录

        # 在 html 目录中写文件
        with open(os.path.join("html", "%s.html" % (file_name)), "w", encoding="utf8") as h:
            h.write(html)

        # 在 docs 目录中写文件
        with open(os.path.join("docs", "%s.md" % (file_name)), "w", encoding="utf8") as m:
            m.write(md)

        # 在 reademe.md 中写文件
        with open("README.md", "w", encoding="utf8") as mm:
            mm.write(md)

        log.logger.info(f"{file_name} 保存成功!")
        return os.path.join("docs", "%s.md" % (file_name)), html

    def parseArticle(self, htmlData):
        '''
        解析文章内容,传入匹配出来的html,转为 markdown 格式
        并保存处理后的HTML MD文件
        '''

        html = self.disposeHTML(htmlData)
        md = html2text.html2text(html)

        return html, md


if __name__ == "__main__":
    sky = SkyTask()
    # sky.writeDoc("# 测试", "<h1>测试</h1>", "1")
