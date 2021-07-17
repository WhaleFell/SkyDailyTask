#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-07-15 22:17:41
LastEditTime: 2021-07-18 00:03:53
Description: 网易大神-光遇每日任务爬虫
'''
import requests
from lxml import etree
import re
import html2text  # html 转 md
# from email_service import EmailService
import os
import time


class SkyTask(object):
    '''获取光遇任务类'''

    def __init__(self) -> None:
        '''初始化方法,用手机UA请求'''
        self.header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36",
        }
        # 光遇小管家主页
        self.index_url = "https://m.ds.163.com/user/95c6340497c7415c9970f94ec14625c6"

    def getIndex(self) -> list:
        '''获取文章链接,返回一个链接列表'''
        resp = requests.get(self.index_url, headers=self.header).text
        # print(resp)
        html = etree.HTML(resp)
        boxs = html.xpath(r"//div[@class='feed-card']")
        urlsList = []
        for box in boxs:
            url = 'https://m.ds.163.com' + \
                box.xpath("//div[@class='feed-brief-card']/a/@href")[0]  # 文章链接
            urlsList.append(url)
        # print(urlsList)
        return urlsList

    def parse(self) -> list:
        '''获取文章详细,返回一个HTML列表'''
        urlList = self.getIndex()
        docs = []
        for url in urlList:
            # print(url)
            resp = requests.get(url, headers=self.header).text
            pat = re.compile(
                r'<article class="feed-article__content">(.*?)</article>')``
            try:
                result = pat.findall(resp)[0]
                # print(result)
                docs.append(result)
            except:
                pass

        return docs

    def disposeHTML(self, html: str):
        '''处理HTML去除头部广告,添加自适应宽度.'''

        AD = '<p align="center"><a href="https://app.16163.com/ds/ulinks/?utm_term=wyds_dl_kf_gy_xy_5cb546a0d5456870b97d9424"><img src="https://ok.166.net/reunionpub/ds/kol/20210717/010312-yo3dnkhpiu.png" width="100%" height="100%"></a></p>'

        # 高宽自适应,匹配所有
        html = re.sub(r'width="[0-9]*"', 'width="100%"', html)
        html = re.sub(r'height="[0-9]*"', 'height="100%"', html)
        html = html.replace(AD, "")  # 删除头部广告

        return html

    def makedir(self):
        '''新建目录'''
        if not os.path.exists("markdown"):
            os.mkdir("markdown")
        if not os.path.exists("html"):
            os.mkdir("html")

    def parseArticle(self, htmlData):
        '''
        解析文章内容,传入匹配出来的html,转为 markdown 格式
        并保存处理后的HTML MD文件
        '''

        self.makedir()
        html = self.disposeHTML(htmlData)
        md = html2text.html2text(html)

        file_name = time.strftime("%Y_%m_%d %H_%M_%S")

        with open(os.path.join("markdown", "%s.md" % (file_name)), "w", encoding="utf8") as f:
            f.write(md)
        with open(os.path.join("html", "%s.html" % (file_name)), "w", encoding="utf8") as f:
            f.write(html)

        return html, md


if __name__ == "__main__":
    sky = SkyTask()
    # mail = EmailService()
    # mail.serviceStatus()
    doc = sky.parse()[0]
    print(doc)
    sky.parseArticle(doc)
