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