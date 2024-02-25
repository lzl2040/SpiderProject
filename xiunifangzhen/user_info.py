import json
from urllib.parse import quote, unquote
import urllib3
import hashlib
import requests
from loguru import logger

def getExpInfo():
    # 这几个都是不变的
    APPID = '105348'
    SECRET = 'bNuKsTVhKwHWL3xzWIfxk1is63VnSfa5sxCnMQDegH0='
    API_PATH = 'http://202.205.145.156:8017'

    # 此处是从Url中获取到的Ticket，需要先进行解码
    TICKET = '22Wedtn1xcQWVAuqqnVOn1IvUlIZZneNQa0bxMqhJuMxkYmo5%2B1UFkxS7PclakS5u3P6cXwrv8%2B7iR7MzVUvuG8WoLpzh0Z2Y2sTx8f3wWQ%3D'
    # 获得signature
    text = unquote(TICKET) + APPID + SECRET
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf8'))
    signature = hl.hexdigest().upper()
    logger.info("signature:" + signature)
    url = API_PATH + '/open/api/v2/token?ticket=' + TICKET + '&appid=' + APPID + '&signature=' + signature
    resp = requests.get(url=url)
    logger.info("返回信息为:" + resp.text)


if __name__ == '__main__':
    getExpInfo()