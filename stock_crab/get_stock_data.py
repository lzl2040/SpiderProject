# -*- encoding: utf-8 -*-
"""
File get_stock_data.py
Created on 2023/9/10 18:42
Copyright (c) 2023/9/10
@author: 
"""
import requests
import json
import argparse
import time
import random
# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header
from email.message import EmailMessage
import ssl
from loguru import logger

class EmailSend():
    def __init__(self,sender,receiver,auth_key):
        self.sender = sender
        self.receiver = receiver
        self.auth_key = auth_key

    def send(self,content):
        # 端口号:465 or 587
        port = 465
        ## qq邮箱不行,网易邮箱可以
        host = "smtp.163.com"
        context = ssl.create_default_context()
        # 正文
        msg = MIMEText(content, 'plain','utf-8')
        # 邮件主题
        msg['Subject'] = "股票阈值通知"  # 邮件主题
        msg['From'] = self.sender
        msg['To'] = ",".join(self.receiver)
        logger.info("开始发送邮件...")
        smtp = smtplib.SMTP_SSL(host,port,context=context)  # 建立和SMTP邮件服务器的连接
        logger.info("连接服务器完成")
        smtp.login(self.sender, self.auth_key)
        logger.info("登录成功")
        smtp.sendmail(self.sender,self.receiver,msg.as_string())
        smtp.quit()
        logger.info("邮件发送完成!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='stock')
    parser.add_argument("--cycle_range", required = False, default = "3-10", help = "Range of periodic changes format: min-max")
    parser.add_argument("--stock_code", required = False, default="AAPL", help = "Stock code")
    parser.add_argument("--pt", required = False, default=12, help="The thresold of the price")
    args = parser.parse_args()
    # 得到周期时间变化的范围
    range_time = args.cycle_range.split('-')
    min_t = int(range_time[0])
    max_t = int(range_time[1])
    url = f"https://api.nasdaq.com/api/quote/{args.stock_code}/info?assetclass=stocks"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.76"
    }
    session = requests.Session()
    # 邮箱相关
    # 授权码
    auth_key = "你的key"
    # 发送者的邮箱
    sender_email = "@163.com"
    # 接收者的邮箱
    receiver_email = ["@qq.com"]
    email_s = EmailSend(sender_email, receiver_email, auth_key)
    while True:
        resp = session.get(url, headers = headers)
        json_str = resp.json()
        main_data = json_str['data']['primaryData']
        cur_price = main_data['lastSalePrice'][1:]
        if float(cur_price) > int(args.pt):
            print(f"当前价格为:{cur_price}")
            # 发送邮件
            email_s.send(f"到达阈值了! 当前价格为:{cur_price}")
        # 睡眠一段时间
        sleep_t = random.randint(min_t, max_t)
        print(f"间隔{sleep_t}s再次发起请求")
        time.sleep(sleep_t)