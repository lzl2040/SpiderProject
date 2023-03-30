import requests
from loguru import logger
from bs4 import BeautifulSoup

# 豆瓣登录
def login():
    # 麻烦的事情:需要滑块验证码
    phone = "34334"
    pwd = "234"
    # phone = input("请输入电话号码")
    # pwd = input("请输入密码")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }
    pay_loads = {
        'name':phone,
        'password':pwd,
        'ticket':"",
        'randstr':"",
        'remember':'true',
        'tc_app_id':""
    }
    login_url = "https://accounts.douban.com/j/mobile/login/basic"
    login_resp = requests.post(url=login_url,headers=headers,data=pay_loads).text
    print(login_resp)

def search_movie():
    search_url = "https://www.douban.com/search?q="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }

    movie_name = input("请输入你要查找的电影名称:")
    search_url += movie_name
    logger.info("搜索电影中....")
    search_resp = requests.get(url=search_url, headers=headers).text
    bs1 = BeautifulSoup(search_resp, "html.parser")
    logger.info("得到搜索电影结果:")
    # 找到第一条符合的
    first_result = bs1.find_all(class_='result')[0]
    # 找到进去的网址
    fitst_result_a = first_result.find('a')['href']
    print('电影评分网址:' + fitst_result_a)
    # 找到基本介绍
    first_intro = first_result.find('p').text
    print('电影介绍为:' + first_intro)
    # 找到评分人数
    first_rating_num = first_result.find(class_='rating_nums').text
    print('评分为:' + first_rating_num)
    first_rating_person = first_result.find(class_='rating-info').find_all('span')[2].text
    print('评分人数为:' + first_rating_person)
    # 找到导演、主演、年份
    first_person_info = first_result.find(class_='subject-cast').text
    print('主要信息:' + first_person_info)
    return fitst_result_a

# 找短评
def find_short_comment(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }
    logger.info("进入电影评分界面")
    movie_resp = requests.get(url=url,headers=headers).text
    bs1 = BeautifulSoup(movie_resp,'html.parser')
    scan_all_url = bs1.select(".mod-hd .pl a")[0]['href']
    logger.info("进入评论界面:" + scan_all_url)
    '''
    参数说明:
        sort:
            new_score:热门评论
            time:最新评论
        start:当前页开始的条数位置(豆瓣超过200条就不展示了)
        limit:每页限制的条数
    '''
    pay_loads = {
        "start": 0,
        "limit": 180,
        "sort": "time"
    }
    short_commet_resp = requests.get(url=scan_all_url,headers=headers,params=pay_loads).text
    # short_commet_resp.encoding = 'utf-8'
    # print(short_commet_resp)
    '''
    豆瓣评分说明:
        1星:很差
        2星:较差
        3星:还行
        4星:推荐
        5星:力荐
    '''
    bs2 = BeautifulSoup(short_commet_resp,'html.parser')
    comments_boxes = bs2.find_all(class_='short')
    comments = []
    logger.info("短评信息如下:")
    for box in comments_boxes:
        comment = box.text
        print(comment)
        comments.append(comment)

if __name__ == '__main__':
    # login()
    target_url = search_movie()
    find_short_comment(target_url)

