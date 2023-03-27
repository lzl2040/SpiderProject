import execjs
import requests
import pytesseract
from PIL import Image
import re
import json
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import time
from loguru import logger
import argparse

'''
选课接口:
    接口:http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?jx0404id=202220232010579&xkzy=&trjf=
    jx0404id是标识课程的一个id
获取课程的接口:
    接口:http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=
    参数:
        sEcho: SpiderProject
        iColumns: 13
        sColumns: 
        iDisplayStart: 0
        iDisplayLength: 15
        mDataProp_0: kch
        mDataProp_1: kcmc
        mDataProp_2: newszkcflmc
        mDataProp_3: xf
        mDataProp_4: skls
        mDataProp_5: sksj
        mDataProp_6: skdd
        mDataProp_7: ktmc
        mDataProp_8: xkrs
        mDataProp_9: syrs
        mDataProp_10: ctsm
        mDataProp_11: szkcflmc
        mDataProp_12: czOper
搜索课程的接口:
    接口:http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=搜索内容&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=
    参数:
        sEcho: SpiderProject
        iColumns: 13
        sColumns: 
        iDisplayStart: 0
        iDisplayLength: 15
        mDataProp_0: kch
        mDataProp_1: kcmc
        mDataProp_2: newszkcflmc
        mDataProp_3: xf
        mDataProp_4: skls
        mDataProp_5: sksj
        mDataProp_6: skdd
        mDataProp_7: ktmc
        mDataProp_8: xkrs
        mDataProp_9: syrs
        mDataProp_10: ctsm
        mDataProp_11: szkcflmc
        mDataProp_12: czOper
'''


def wenhuasuzhi(session,header):
    # 点击公选课选课
    url = 'http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=&skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb='
    data = {
        "sEcho": 1,
        "iColumns": 13,
        "sColumns":"",
        "iDisplayStart": 0,
        "iDisplayLength": 200,
        "mDataProp_0": "kch",
        "mDataProp_1": "kcmc",
        "mDataProp_2": "newszkcflmc",
        "mDataProp_3": "xf",
        "mDataProp_4": "skls",
        "mDataProp_5": "sksj",
        "mDataProp_6": "skdd",
        "mDataProp_7": "ktmc",
        "mDataProp_8": "xkrs",
        "mDataProp_9": "syrs",
        "mDataProp_10": "ctsm",
        "mDataProp_11": "szkcflmc",
        "mDataProp_12": "czOper"
    }
    header['Referer'] = 'http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/comeInGgxxkxk'
    ## 使用params参数
    logger.info('选择公选课选课')
    course_info_resp = session.post(url=url,params=data,headers=header)
    course_info_resp.encoding = 'utf-8'
    json_info = course_info_resp.json()
    course_info = json_info['aaData']
    logger.info('可选的课程有:')
    for course in course_info:
        remain_num = int(course['syrs'])
        if remain_num > 0:
            print(course['kcmc'] + ':' + course['syrs'])
    ## 转换为json格式
    search_content = args.course_name
    ## 进行两次URL编码
    search_content = urllib.parse.quote(search_content)
    search_content = urllib.parse.quote(search_content)
    logger.info('搜索内容的编码信息:' + search_content)
    search_url = 'http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?skls=&skxq=&skjc=&sfym=false&sfct=false&szjylb=&sEcho=1&iColumns=13&sColumns=&iDisplayStart=0&iDisplayLength=15&mDataProp_0=kch&mDataProp_1=kcmc&mDataProp_2=newszkcflmc&mDataProp_3=xf&mDataProp_4=skls&mDataProp_5=sksj&mDataProp_6=skdd&mDataProp_7=ktmc&mDataProp_8=xkrs&mDataProp_9=syrs&mDataProp_10=ctsm&mDataProp_11=szkcflmc&mDataProp_12=czOper&kcxx='
    search_url += search_content
    '''
        存在一个问题:输入中文后编码的部分作为参数,得不到响应
        解决办法:
            SpiderProject.就使用get请求,不使用post方法提交表单数据
            2.想用post,但是输入中文还是没有数据
    '''
    logger.info('发送搜索参数')
    search_response = session.get(url=search_url,headers=header)
    search_response.encoding = 'utf-8'
    search_resp_json = search_response.json()
    search_res = search_resp_json['aaData']
    ## 获得课程id,用于抢课
    if len(search_res) > 0:
        logger.info('开始选课')
        first_res_id = search_res[0]['jx0404id']
        first_res_name = search_res[0]['kcmc']
        logger.info('课程名字:' + first_res_name + " 课程id:" + first_res_id)
        # 开始选课
        grap_course_url = 'http://jwxt.xtu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?xkzy=&trjf=&jx0404id='
        grap_course_url += first_res_id
        grap_resp = session.get(url=grap_course_url,headers=header)
        grap_resp.encoding = 'utf-8'
        grap_resp_json = grap_resp.json()
        logger.info('选课状态信息:' + str(grap_resp_json))
        condition = grap_resp_json['success']
        if condition == True:
            logger.info('抢课成功')
        else:
            logger.warning('抢课失败')
    else:
        logger.warning('没有搜到该课程')

def kuaxiaogongxiang(session,header):
    pass


def get_img_code():
    """
    获得验证码
    :return:4位的验证码
    """
    logger.info("获取验证码中...")
    headers['Content-Type'] = 'image/jpeg;charset=UTF-8'
    code_response = session.get("http://jwxt.xtu.edu.cn/jsxsd/verifycode.servlet", headers=headers)
    code_binary = code_response.content
    # 保存验证码图片
    with open("./code_img.png", 'wb') as f:
        f.write(code_binary)
    f.close()
    code_img = Image.open('./code_img.png')
    text = pytesseract.image_to_string(code_img, lang='chi_sim')
    routine = re.compile('[0-9a-zA-Z]')
    random_code = re.findall(routine, text)
    if len(random_code) != 4:
        return None
    else:
        return random_code

def login(name,pwd,i):
    """
    登录的程序
    :param name: 用户名
    :param pwd: 密码
    :param i:迭代次数
    :return:
        0:登录成功
        SpiderProject:登录失败
    """
    logger.info('获取加密参数')
    data = {
        'USERNAME': name,
        'PASSWORD': pwd
    }
    response = session.post("http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk?flag=sess", headers=headers).json()
    encoded = execjs.compile(open('./jwxt_encode.js', 'r', encoding='utf-8').read()).call('encode', response['data'],
                                                                                          name, pwd)
    logger.info('加密参数为:'+encoded)
    data['encoded'] = encoded
    # 获得验证码
    random_code = get_img_code()
    if random_code == None:
        logger.warning("获取验证码失败")
        return 1
    else:
        codes = random_code[0] + random_code[1] + random_code[2] + random_code[3]
        logger.info("获取的验证码为:"+codes)
        data['RANDOMCODE'] = codes
        logger.info("参数加载完成,发送登录请求")
        main_page = session.post("http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk", headers=headers, params=data)
        resp_bs = BeautifulSoup(main_page.text,'html.parser')
        xuehao_box = resp_bs.find(id='xh')
        # print(xuehao_box)
        if xuehao_box != None:
            # 登录失败
            logger.warning('第%d次尝试:登录失败' % i)
            return 1
        else:
            # 登录成功
            logger.info('第%d次尝试:登录成功' % i)
            return 0

def enter_main_page():
    # 进入选课界面
    logger.info("进入选课界面")
    choose_course_page_entry = session.get('http://jwxt.xtu.edu.cn/jsxsd/xsxk/xklc_list', headers=headers)
    # print(choose_course_page_entry.text)
    bs1 = BeautifulSoup(choose_course_page_entry.text, 'html.parser')
    # 找到选课的几个表格
    logger.info("找到选课表格")
    choose_course_table = bs1.select('#tbKxkc tr')
    ## 删除第一个元素
    choose_course_table.pop(0)
    # print(len(choose_course_table))
    choose_course_name = []
    choose_course_link = []
    print('选课中心内容展示如下:')
    for line_tr in choose_course_table:
        # print(line_tr)
        name = line_tr.find_all('td')[1].text
        course_link = line_tr.find_all('td')[3].find_all('a')[0]['href']
        choose_course_link.append(host + course_link)
        choose_course_name.append(name)
        print(name + ":" + host + course_link)
    number = args.choice
    course_page = session.get(choose_course_link[number - 1], headers=headers)
    if number == 1:
        # 文化素质教育课程选课
        wenhuasuzhi(session, header=headers)
    elif number == 2:
        kuaxiaogongxiang(session, header=headers)
        print('暂未开发')
    elif number == 3:
        print('暂未开发')
    elif number == 4:
        print('暂未开发')
    # print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='you need input these params:')
    parser.add_argument("--name","-name",type=str,help='用户名',required=True)
    parser.add_argument('--pwd','-pwd',type=str,help='你的密码',required=True)
    parser.add_argument('--choice','-choice',type=int,help='你要选择的课程类型,默认为文化素质',default=1)
    parser.add_argument('--course_name','-course_name',type=str,help='你要选项的课程名字',required=True)
    parser.add_argument('--it','-it',type=str, help='发送请求的次数,避免验证码错误',default=30)
    args = parser.parse_args()
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Host': 'jwxt.xtu.edu.cn',
        'Referer': 'http://jwxt.xtu.edu.cn/jsxsd/xk/LoginToXk',
        'Upgrade-Insecure-Requests': 'SpiderProject',
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'X-Requested-With': "XMLHttpRequest",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47',
    }
    host = 'http://jwxt.xtu.edu.cn/jsxsd/'
    # 这个会自动获得一个session
    logger.info('开始创建会话')
    session = requests.Session()

    # 输入数据
    # name = input("请输入用户名:")
    # pwd = input("请输入密码:")
    logger.info('用户名和密码已加载')
    name = args.name
    pwd = args.pwd
    iterations = args.it
    logger.info('开始迭代')
    for i in range(iterations):
        logger.info('第%d次登录:' % i)
        flag = login(name,pwd,i)
        if flag == 0:
            # 登录成功进入主界面
            enter_main_page()
            break
        elif flag == 1:
            # 验证码错误,重新刷新获取验证码,注意name和pwd也要重新发给服务器
            continue