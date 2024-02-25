# -*- encoding: utf-8 -*-
"""
File Login.py
Created on 2023/9/18 10:47
Copyright (c) 2023/9/18
@author: 
"""
import base64

import requests
import rsa
import re
from loguru import logger
# 学院多选的情况
## type=&deptIds=921&deptIds=951&courseCode=180086081200P1006H-1&courseName=%E9%AB%98%E7%BA%A7%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B
# 保存课程时课程多选的情况
## deptIds=951&sids=7178E2FC9538CA98&sids=DE42EB9AC25160C1&vcode=18
class Login:
    def __init__(self, username,pwd, dept_id, c_name, course_code = ""):
        self.name = username
        # 每次生成的不一样
        self.pwd = self.enctrypt_pwd(pwd)
        self.c_code = course_code
        self.d_id = dept_id
        self.c_name = c_name
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.69",
            "Host": "sep.ucas.ac.cn",
            "Referer": "https://sep.ucas.ac.cn/",
            "Connection": "keep-alive"
        }
        self.login_params = {
            "userName": self.name,
            "pwd": self.pwd,
            "loginForm": "",
            # "certCode": "",
            "sb" : "sb"
        }
        # 选课的参数
        self.select_params = {
            "type": "",
            "deptIds": self.d_id,
            "courseCode": "",
            "courseName": self.c_name
        }
        # 保存选课的参数
        self.save_params = {
            "deptIds": self.d_id,
            "sids": "",
            "vcode": ""
        }
        self.session.headers.update(self.headers)

    def enctrypt_pwd(self, pwd):
        jsePubKey = """
        -----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxG1zt7VW/VNk1KJC7AuoInrMZKTf0h6S6xBaROgCz8F3xdEIwdTBGrjUKIhIFCeDr6esfiVxUpdCdiRtqaCS9IdXO+9Fs2l6fx6oGkAA9pnxIWL7bw5vAxyK+liu7BToMFhUdiyRdB6erC1g/fwDVBywCWhY4wCU2/TSsTBDQhuGZzy+hmZGEB0sqgZbbJpeosW87dNZFomn/uGhfCDJzswjS/x0OXD9yyk5TEq3QEvx5pWCcBJqAoBfDDQy5eT3RR5YBGDJODHqW1c2OwwdrybEEXKI9RCZmsNyIs2eZn1z1Cw1AdR+owdXqbJf9AnM3e1CN8GcpWLDyOnaRymLgQIDAQAB
        -----END PUBLIC KEY-----
        """
        # 使用 rsa 模块创建加密对象
        encryptor = rsa.encrypt
        # 将公钥字符串解码为字节流
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(jsePubKey.encode('utf-8'))
        # 对密码进行加密
        passwordRSA = encryptor(pwd.encode('utf-8'), pub_key)
        # 将加密后的密码转换为 Base64 字符串（可选）
        passwordRSABase64 = base64.b64encode(passwordRSA).decode('utf-8')
        return passwordRSABase64
    def save_img(self, img_info, name):
        with open(f'{name}','wb') as f:
            f.write(img_info)

    def generate_select_cookie(self):
        cookie_dict = {
            cookie.name: cookie.value
            for cookie in self.session.cookies if 'undefined' not in cookie.value
        }
        cookie_dict["org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE"] = "zh_CN"
        self.select_cookie = '; '.join([name + '=' + cookie_dict[name] for name in cookie_dict])
        # 保存
        with open("select_cookie.txt", "w") as f:
            f.write(self.select_cookie)

    def run(self):
        # 获取验证码
        # verfify_code_url = "https://sep.ucas.ac.cn/changePic"
        # img_resp = self.session.get(verfify_code_url)
        # img_binary = img_resp.content
        # self.save_img(img_binary, "login.png")
        # # 手动输入验证码 / 自动识别(未做)
        # vcode = input("请输入登录验证码:")
        # self.login_params["certCode"] = vcode
        # 登录
        login_url = "https://sep.ucas.ac.cn/slogin"
        _ = self.session.post(login_url, data = self.login_params)
        select_course_enter_url = "http://sep.ucas.ac.cn/portal/site/226/821"
        sce_resp = self.session.get(select_course_enter_url, timeout = 10)
        # 判断是否登录成功
        # identity = re.findall("https://jwxkts2.ucas.ac.cn/login\?Identity=(.*?)&roleId", sce_resp.text, re.S)
        identity = re.findall("https://xkcts.ucas.ac.cn//login\?Identity=(.*?)&roleId", sce_resp.text, re.S)
        if len(identity) == 0:
            logger.warning("登录失败！请重新登录")
        else:
            identity = identity[0]
            logger.info(f"identity is:{identity}")
            # 得到新的session id
            pre_url1 = "https://xkcts.ucas.ac.cn//login?Identity=" + identity +"&roleId=821"
            self.session.get(pre_url1, timeout = 10)
            self.generate_select_cookie()
            # 选课
            self.select_course()

    def refresh_status(self):
        select_course_enter_url = "http://sep.ucas.ac.cn/portal/site/226/821"
        sce_resp = self.session.get(select_course_enter_url, timeout=10)
        # 判断是否登录成功
        identity = re.findall("https://xkcts.ucas.ac.cn/login\?Identity=(.*?)&roleId", sce_resp.text, re.S)
        identity = identity[0]
        logger.info(f"identity is:{identity}")
        # 得到新的session id
        pre_url1 = "https://xkcts.ucas.ac.cn/login?Identity=" + identity + "&roleId=821"
        self.session.get(pre_url1, timeout=10)
        self.generate_select_cookie()


    def select_course(self):
        # 进入选课系统主界面
        select_course_main_url = "https://xkcts.ucas.ac.cn/courseManage/main"
        # 1.更新headers
        self.session.headers["Cookie"] = self.select_cookie
        # print(self.session.headers["Cookie"])
        self.session.headers["Host"] = "jwxkts2.ucas.ac.cn"
        self.session.headers["Referer"] = "https://xkcts.ucas.ac.cn/notice/view/1"
        select_main_resp = self.session.get(select_course_main_url)
        # 2.找到选课的入口
        select_url_pattern = r"selectCourse\?s=(.*?)\""
        self.s_name = re.findall(select_url_pattern, select_main_resp.text)[0]
        logger.info(f"params s: {self.s_name}")
        select_course_url = "https://xkcts.ucas.ac.cn/courseManage/selectCourse?s=" + self.s_name
        self.session.headers["Referer"] = select_course_url
        # 3.进入选课界面
        select_course_resp = self.session.post(select_course_url, data = self.select_params)
        c_sid,c_name = self.get_course_sid(select_course_resp.text, self.c_code)
        logger.info(f"课程编码:{self.c_code}对应的课程:{c_name}的sid为:{c_sid}")
        # 4.读取选课验证码
        select_img_url = "https://xkcts.ucas.ac.cn/captchaImage"
        select_img_resp = self.session.get(select_img_url)
        img_binary = select_img_resp.content
        self.save_img(img_binary, "select_img.png")
        select_vcode = input("请输入选课验证码:")
        # 5.保存选课
        self.save_params["vcode"] = select_vcode
        self.save_params["sids"] = c_sid
        self.session.headers["Referer"] = select_course_url
        self.session.headers["Origin"] = "https://xkcts.ucas.ac.cn"
        save_course_url = "https://xkcts.ucas.ac.cn/courseManage/saveCourse?s=" + self.s_name
        save_course_resp = self.session.post(save_course_url, data=self.save_params)
        # 更新session id
        self.refresh_status()

    def get_course_sid(self, resp_text, c_code):
        # 匹配的模式
        c_code_pt = r"<span id=\"courseCode_.*?\">(.*?)</span>"
        c_sid_pt = r"<span id=\"courseCode_(.*?)\">"
        c_name_pt = r"<a href=\"/course/coursetime/.*?\" target=\"_blank\">(.*?)</a>"
        c_id_pt = r"<a href=\"/course/coursetime/(.*?)\""
        # c_limit_stu_pt = r"courseCredit_.*?<td>(.*?)</td>.*?>.*?</td>"
        # c_select_stu_pt = r"courseCredit_.*?<td>.*?</td>.*?>(.*?)</td>"
        # 得到匹配的结果
        c_codes = re.findall(c_code_pt, resp_text)
        c_sids = re.findall(c_sid_pt, resp_text)
        c_names = re.findall(c_name_pt, resp_text)
        c_ids = re.findall(c_id_pt, resp_text)
        # c_limit_stus = re.findall(c_limit_stu_pt, resp_text)
        # c_select_stus = re.findall(c_select_stu_pt, resp_text)
        course_dict = {}
        if len(c_codes) == 0:
            logger.warning("获取课程列表失败")
            return None
        else:
            for i in range(len(c_codes)):
                course_dict[c_codes[i]] = [c_sids[i], c_names[i], c_ids[i]]
        return course_dict[c_code][0], course_dict[c_code][1]

if __name__ == '__main__':
    # 从deptId=951的院系中选取courceId=180086081200P1006H-1的课
    # 人工智能学院：969
    # 计算机学院：951
    login_sess = Login("lizuolei23@mails.ucas.ac.cn","LZLYXM20",951, "视觉信息学习与分析", "180086081203P4003H")
    login_sess.run()