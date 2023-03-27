import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import re
if __name__ == '__main__':
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    # 定义表头
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
    }
    # 创建一个会话
    session = requests.Session()
    # 进入登录界面
    login_resp = session.post(url=url,headers=headers)
    # 获得登录界面源代码
    login_html = login_resp.text
    # print(login_html)
    # 解析数据
    bs = BeautifulSoup(login_html,'html.parser')
    # 找到__VIEWSTATE和__VIEWSTATEGENERATOR并获得数据
    VIEWSTATE = bs.find(id = "__VIEWSTATE")
    print(VIEWSTATE.get("value"))
    VIEWSTATEGENERATOR = bs.find(id = "__VIEWSTATEGENERATOR")
    print(VIEWSTATEGENERATOR.get("value"))
    # 获得验证码图片
    code_img_data = session.get('https://so.gushiwen.cn/RandCode.ashx',headers=headers).content
    # 保存验证码
    with open("code.png","wb") as f:
        f.write(code_img_data)
    f.close()
    # 识别验证码
    code_img = Image.open('code.png')
    text = pytesseract.image_to_string(code_img, lang='chi_sim')
    routine = re.compile('[0-9a-zA-Z]')
    random_code = re.findall(routine, text)
    data = {}
    if len(random_code) != 4:
        print('error')
    else:
        codes = random_code[0] + random_code[1] + random_code[2] + random_code[3]
        print('验证码是:' + codes)
        data['code'] = codes
        data['__VIEWSTATE'] = VIEWSTATE
        data['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR
        data['from'] = 'http://so.gushiwen.cn/user/collect.aspx'
        data['denglu'] = '登录'
        email = input("请输入邮箱:")
        pwd = input("请输入密码:")
        data['email'] = email
        data['pwd'] = pwd
        # 进行登录
        login_response = session.post(url=url,headers=headers,data=data)
        resp_text = login_response.text
        print(resp_text)

