# -*- encoding: utf-8 -*-
"""
File auto_detect.py
Created on 2024/2/19 0:02
Copyright (c) 2024/2/19
@author:
"""
# -- coding:UTF-8 --
import os
import time
from bs4 import BeautifulSoup
from splinter import Browser
import smtplib
import ssl
from email.mime.text import MIMEText
from loguru import logger
from datetime import datetime

class EmailSend():
    def __init__(self,sender,receiver,auth_key):
        self.sender = sender
        self.receiver = receiver
        self.auth_key = auth_key

    def send(self, content, subject):
        # 端口号:465 or 587
        port = 465
        ## qq邮箱不行,网易邮箱可以
        host = "smtp.163.com"
        context = ssl.create_default_context()
        # 正文
        msg = MIMEText(content, 'plain','utf-8')
        # 邮件主题
        msg['Subject'] = subject  # 邮件主题
        msg['From'] = self.sender
        msg['To'] = ",".join(self.receiver)
        try:
            logger.info("开始发送邮件...")
            smtp = smtplib.SMTP_SSL(host,port,context=context)  # 建立和SMTP邮件服务器的连接
            logger.info("连接服务器完成")
            smtp.login(self.sender, self.auth_key)
            logger.info("登录成功")
            smtp.sendmail(self.sender,self.receiver,msg.as_string())
            smtp.quit()
            logger.info("邮件发送完成!")
        except:
            logger.error("Error: 无法发送邮件")

class ScholarOneManuscriptListener:
    def __init__(self, email_con, trans_type, name, pwd, delay_time, interval):
        # chrome浏览器的驱动器exe地址
        self.driver_path = "chromedriver.exe"
        self.email_con = email_con
        self.trans_type = trans_type
        self.name = name
        self.pwd = pwd
        self.interval = interval
        self.wait_delay = delay_time
        self.save_file = "log.txt"

    def get_last_status(self):
        status = "NULL"
        iter = 0
        with open(self.save_file, "r") as f:
            content = f.readline()
            if content != "":
                _, iter, status = content.strip().strip(",")
        return int(iter), status

    def run(self):
        logger.info("-" * 100)
        logger.info(f"发送请求的间隔时间：{self.interval}s")
        logger.info("-" * 100)
        iter, current_status = self.get_last_status()
        while True:
            try:
                logger.info("-" * 50 + f"第{iter}迭代" + "-" * 50)
                time_remaining = self.interval - time.time() % self.interval

                logger.info(f"休眠停止时间：{datetime.fromtimestamp(time.time() + time_remaining).strftime('%Y:%m:%d')} ({time_remaining}s)...")
                time.sleep(time_remaining)
                current_status = self.refresh_status(current_status, iter)
                logger.info("-" * 50 + f"第{iter}迭代" + "-" * 50)
                iter += 1
            except Exception:
                logger.error("未知的Error")

    def refresh_status(self, status, iter):
        previous_manuscript_status = status

        logger.info('之前的投稿状态为: ' + previous_manuscript_status)
        time.sleep(self.wait_delay)

        b = Browser('chrome', headless=True, executable_path=self.driver_path)
        time.sleep(self.wait_delay)
        logger.info("访问网站...")
        b.visit(f'https://mc.manuscriptcentral.com/{trans_type}')  # 此处设置scholar one对应期刊的网址
        time.sleep(self.wait_delay)
        logger.info("输入账号、密码...")
        b.fill('USERID', username)  # 此处设置你的scholar one账号邮箱
        time.sleep(self.wait_delay)
        b.fill('PASSWORD', pwd)  # 此处设置你的scholar one账号密码
        time.sleep(self.wait_delay)
        logger.info("点击登录按钮...")
        b.find_by_id('logInButton').click()
        time.sleep(self.wait_delay)
        logger.info("点击Author界面...")
        b.links.find_by_partial_href('AUTHOR').click()
        time.sleep(self.wait_delay)
        html_obj = b.html
        soup = BeautifulSoup(html_obj, "lxml")
        # 状态显示位置的元素
        table = soup.find("span", attrs={"class": "pagecontents"})
        current_manuscript_status = table.string
        logger.info(f"当前的投稿状态为:{table.string}")
        # 写入文件
        with open(self.save_file, "a") as f:
            content = f"{datetime.now().strftime('%Y-%m-%d %H:%M')},{iter},{table.string}\n"
            f.write(content)
        time.sleep(self.wait_delay)
        b.quit()
        if current_manuscript_status == previous_manuscript_status:
            logger.info('您的投稿状态没有改变 ...')
        else:
            logger.info("投稿状态已改变，将发邮件通知您 ...")
            message = f'投稿状态已改变: \n{current_manuscript_status}\n 查看网址：https://mc.manuscriptcentral.com/{self.trans_type}/'
            subject = f'{trans_type}: 投稿状态'
            self.email_con.send(message, subject)
            previous_manuscript_status = current_manuscript_status

        return current_manuscript_status

if __name__ == "__main__":
    # 邮箱授权码 POP3/SMTP服务
    auth_key = "你的邮箱key"
    # 发送者的邮箱
    sender_email = "@163.com"
    # 接收者的邮箱
    receiver_email = ["@qq.com"]
    email_con = EmailSend(sender_email, receiver_email, auth_key)
    trans_type = "tcsvt"
    username = "@163.com"
    pwd = "你的密码"
    # 此处设置间隔时间
    interval = 5
    listener = ScholarOneManuscriptListener(email_con, trans_type, username, pwd, 1, interval)
    listener.run()

    # test()


