from Crypto.Cipher import AES # pip install pycryptodome
from base64 import b64encode
import requests
import json

i="gcbRwuLzJcbzxAPC"
def get_ensSecKey():
    return "24caa54f2cccf556753a02162ae1f2c37d9ae4af3289e9b773100a3c2d284b94232ac513680119fdb38b3551f18f1e6bb6fd00d49507502da30df2e0d361e01c702be2dd4b31a97a25e95f00e2cdd5663a6ba0e6b328dd073d1c5e1b2a0278accce59c3645065ef1f61e965ef505e8f9842e8f1e0680242e511b8fc37aadc522"
def get_params(data):
    first=enc_params(data,g); #d中的第一次加密
    secend=enc_params(first,i);#d中的第二次加密
    return secend

def to_16(data):
    pad=16-len(data)%16;
    data+=chr(pad)*pad
    return data
#模拟加密过程
def enc_params(data,key):
    aes = AES.new(key=key.encode('utf-8'),iv="0102030405060708".encode('utf-8'),mode=AES.MODE_CBC)
    data = to_16(data)
    bs = aes.encrypt(data.encode('utf-8')) #加密的内容长度必须是16的倍数
    return str(b64encode(bs),"utf-8")

if __name__ == '__main__':
    # 第一个参数
    data = {
        "csrf_token": "",
        "cursor": "-1",
        "offset": "0",
        "orderType": "1",
        "pageNo": "1",
        "pageSize": "20",
        "rid": "R_SO_4_472603422",
        "threadId": "R_SO_4_472603422"
    }
    # 第二个参数
    e = '010001'
    # 第三个参数
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    # 第四个参数
    g = '0CoJUm6Qyw8W8jud'
    url='https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    resp=requests.post(url,data={
        "params":get_params(json.dumps(data)),
        "encSecKey":get_ensSecKey()
    })
    resp.encoding='utf-8'
    dic=resp.json()
    comments=dic['data']['hotComments']
    for comment in comments:
        content=comment['content']
        print(content)
        #break;测试用
