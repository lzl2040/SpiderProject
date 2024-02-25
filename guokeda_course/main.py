# -*- encoding: utf-8 -*-
"""
File main.py
Created on 2023/9/9 21:36
Copyright (c) 2023/9/9
@author: 
"""
import requests
from bs4 import BeautifulSoup
import re
import cv2
def get_course_sid(target_name, resp_text):
    pt_sid = r"<td><input type=\"checkbox\" name=\"sids\" value=\"(.*?)\" /></td>"
    sids_list = re.findall(pt_sid, resp_text)
    pt_cname = r"<td><a href=\"/course/coursetime/(.*?)</a>"
    names_list = re.findall(pt_cname, resp_text)
    target_sid = ""
    for index in range(len(names_list)):
        c_name = names_list[index].split(">")[1]
        if c_name == target_name:
            target_sid = sids_list[index]
            break
    return target_sid

if __name__ == '__main__':
    s_para = "dee740de-5397-44dc-9482-f083c1b92084"
    # 选课界面的网址
    select_url = "https://jwxkts2.ucas.ac.cn/courseManage/selectCourse?s=" + s_para
    # 验证码的接口
    img_url = "https://jwxkts2.ucas.ac.cn/captchaImage"
    # 提交课程地址
    save_url = "https://jwxkts2.ucas.ac.cn/courseManage/saveCourse?s=" + s_para
    save_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "100",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "jwxkts2.ucas.ac.cn",
        "Origin": "https://jwxkts2.ucas.ac.cn",
        "Referer": "https://jwxkts2.ucas.ac.cn/courseManage/main",
        "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116\"",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "Android",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.69"
    }
    # 加载cookie
    with open("cookie.txt", "r", encoding="utf-8") as f:
        cookie = f.read()
    save_headers["Cookie"] = cookie
    # 选择课程的请求头
    select_headers = dict(save_headers)
    select_headers["Referer"] = select_url
    select_headers.pop("Origin")
    # 选择课程界面的参数
    select_payloads = {
        "type": "",
        "deptIds": 951,
        "courseCode": "",
        "courseName": ""
    }
    # 提交选课的参数
    save_payloads = {
        "deptIds": 951,
        "sids": "",
        "vcode": ""
    }
    session = requests.Session()
    session.headers['Cookie'] = cookie

    # 读取验证码
    # img_headers = dict(save_headers)
    # img_headers["Referer"] = select_url
    # img_headers["Accept"] = "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
    # img_headers["Sec-Fetch-Dest"] = "image"
    # img_headers["Sec-Fetch-Dest"] = "no-cors"
    # img_headers.pop("Upgrade-Insecure-Requests")
    # img_headers.pop("Origin")
    # img_headers.pop("Content-Length")
    # img_headers.pop("Content-Type")
    # img_headers.pop("Cache-Control")
    # img_resp = session.get(img_url, headers=img_headers)
    # img_binary = img_resp.content
    # # 保存验证码图片
    # with open("./select_img.png", 'wb') as f:
    #     f.write(img_binary)
    # vertify_code = input("请输入验证码:")

    # 发起请求 post请求使用data，使用params会无法得到请求
    resp = session.post(select_url, headers=select_headers, data=select_payloads)
    # 读取resp.text内容，找到课程对应的sids
    # course_name = input("请输入课程名字(不能出错):")
    course_name = "图像处理"
    target_sid = get_course_sid(course_name, resp.text)
    print(f"{course_name}对应的sid为：{target_sid}")
    # 保存sid
    save_payloads["sids"] = target_sid

    # save_payloads["vcode"] = vertify_code
    # 确认选课
    save_headers["Referer"] = select_url
    # print(save_headers)
    resp = session.post(save_url, headers=save_headers, data=save_payloads)
    print(resp.text)
