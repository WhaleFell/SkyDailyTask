#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-07-18 11:18:44
LastEditTime: 2021-07-22 17:35:09
Description: 主运行模块
'''
from types import MemberDescriptorType
from email_service import EmailService
from api_web import SkyTask
from log import log
import sqlite3
import os


def writeSQL(title, url, html) -> bool:
    '''写入数据库'''

    conn = sqlite3.connect("weibo.db")
    c = conn.cursor()

    # 新建SkyDaily表,设置主键为 url
    c.execute('''create table if not exists `{}` (
        `title` varchar(225),
        `url` varchar(225),
        `html` varchar(225),
        primary key(`url`)
    )
    '''.format("SkyDaily"))
    conn.commit()

    try:
        # 列表不能为 varchar 类型
        c.execute('''
        insert into `{}` (title,url,html) values (?,?,?)
        '''.format("SkyDaily"), (title, url, html))
        conn.commit()

    except sqlite3.IntegrityError:
        # log.logger.warning(f"{url}数据已存在")
        return False
    except Exception as e:
        log.logger.critical(f"{url}其他错误: {e}")
        return False
    else:
        log.logger.info(f"发现新数据{url}插入成功！")
        return True


def main():
    '''主运行函数'''
    log.logger.info("爬取开始ing......")
    # 各种实例化
    mail = EmailService()
    spider = SkyTask()
    # 获取链接列表,循环直至成功,应对复杂的网络环境
    for i in range(11):
        urls = spider.getIndex()
        if urls:
            break

    log.logger.info(f"共获取到{len(urls)}条链接.")

    urls.reverse()  # 列表倒叙,从旧到新
    count = 0
    for url in urls:
        # 解析单个文章
        # 重试
        for i in range(11):
            title, html = spider.parse(url)
            if html:
                break

        # 处理
        html, md = spider.parseArticle(html)

        # 入库
        if writeSQL(title, url, html):
            count += 1
            # 写入文件
            md_path, html_content = spider.writeDoc(md, html, title)
            mail.send_emails(html_content, fileList=[md_path, "run.log"]) # 支持多邮箱发送.

    log.logger.info(f"处理完成! 新数据条数:{count}")


if __name__ == "__main__":
    main()
