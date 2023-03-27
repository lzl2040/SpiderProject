from Crypto.Cipher import AES # pip install pycryptodome
from base64 import b64encode
import requests
import json

def getSecKey():
    return "2b8c2269fcbce17e7a6359c434a2c6239126635f5d8d4aee88f657d3217f9baff61983439333c8cc22413031fc702a62286148801a06e25b61b97fb209146b75b70d885fdc232d2c6275bce25f4e78fc4e3347da1fc3e533dffd72babba03febd17c7dec3699765654dab11df950e685b1f1fade089330ee6e2c65dae8faade7"

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
    # 搜索接口
    url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    data = {
        "csrf_token":"",
        "hlposttag":"</span>",
        "hlpretag":"<span class=\"s-fc7\">",
        "limit":"30",
        "offset":"0",
        "s":"你好",
        "total":"true",
        "type":"SpiderProject"
    }
    i = 'I6URGZUIZOwsWwdG'
    e = '010001'
    f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    g = '0CoJUm6Qyw8W8jud'
    post_data = {}
    post_data['params'] = get_params(json.dumps(data))
    post_data['encSecKey'] = getSecKey()
    resp = requests.post(url=url, data=post_data)
    resp.encoding = 'utf-8'
    json_resp = resp.json()
    songs = json_resp['result']['songs']
    for song in songs:
        song_id = song['id']
        song_name = song['name']
        print(song_id,song_name)
    # print(resp.text)
