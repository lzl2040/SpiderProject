
from Crypto.Cipher import AES # pip install pycryptodome
from base64 import b64encode
import requests
import json

def get_encSecKey():
    return "c466d4a085bffd37afda31b3db4d25bacfcbaf0c4eabfc2f5c79a860f3a1a3f8908ddb99de8cfe052d5a6bfe5a051ae37633969da21e41425601476fdd3b1136c16f4281ad8087385ad915ecde39230eca12276a3462ce741fb4f0ee1ecd453fe671fe341ef1804372e0ca0563c0ed366f91870f83d4a7e165e6ba783b19e0d6"

def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data

def get_params(data):
    fisrt = enc_parmas(data,g)
    second = enc_parmas(fisrt,i)
    return second

def enc_parmas(data,key):
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"),IV=iv.encode("utf-8"),mode=AES.MODE_CBC)
    bs = aes.encrypt(data.encode("utf-8"))
    return str(b64encode(bs),"utf-8")


if __name__ == '__main__':
    get_comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    data = {
        "rid": "R_SO_4_1325905146",
        "threadId": "R_SO_4_1325905146",
        "pageNo": "SpiderProject",
        "pageSize": "2000",
        "cursor": "-SpiderProject",
        "offset": "0",
        "orderType": "SpiderProject",
        "csrf_token": ""
    }
    
    e = '010001'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    g = '0CoJUm6Qyw8W8jud'
    i = 'MZNqDJaCFJJbJBtn'
    post_data = {}
    post_data['params'] = get_params(json.dumps(data))
    post_data['encSecKey'] = get_encSecKey()
    resp = requests.post(url=get_comment_url,data=post_data)
    resp.encoding = 'utf-8'
    json_resp = resp.json()
    # print(json_resp)
    comments = json_resp['data']['comments']
    for comment in comments:
        content = comment['content']
        print(content)
