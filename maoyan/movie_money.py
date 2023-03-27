import requests
import json
import math
import random
import time
import hashlib
from loguru import logger
import json
import re
from fontTools.ttLib import TTFont
from PIL import ImageFont,Image,ImageDraw
import io
import ddddocr
import prettytable as pt
import time
import pandas as pd
import os

#重点:字体反扒,js逆向

class Movie():
    def __init__(self,name,all_tickets,today_tikets,slice_arr,release_day,ticket_ratio):
        self.name = name
        self.all_tickets = all_tickets
        self.today_tickets = today_tikets
        self.slice_arr = slice_arr
        self.release_day = release_day
        self.ticket_ratio = ticket_ratio

    def showInfo(self):
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.name,self.all_tickets,self.today_tickets,self.slice_arr,self.release_day,self.ticket_ratio))

    def asList(self):
        return [self.name,self.all_tickets,self.today_tickets,self.slice_arr,self.release_day,self.ticket_ratio]


class MaoyanMovieSpider():
    def __init__(self,mode = 0,name = None,time_span = None,sleep_time_max = 60):
        self.base_url = "https://piaofang.maoyan.com/dashboard-ajax"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.56"
        }
        # 请求头参数
        '''
            请求头参数:
                orderType:默认为0
                uuid:是定值
                timeStamp:时间戳,不是定值
                User-Agent:对于一次会话来说是定值
                index:不是定值,是一个随机数
                channelId:是定值,40009
                sVersion:是定值,2
                signKey:不是定值,使用了加密  
        '''
        self.pay_loads = {
            'orderType' : 0,
            'uuid': '1868d965f24c8-0be5317ef150b3-74525470-144000-1868d965f24c8',
            'User-Agent': "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMC4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMTAuMC4xNTg3LjU2",
            'sVersion' : 2,
            'channelId': 40009
        }
        # 用于产生d参数
        self.key = 'A013F70DB97834C0A5492378BD76C53A'
        self.ocr = ddddocr.DdddOcr()
        self.mode = mode
        # 要记录的电影名字
        self.movie_name = name
        # 记录的时间跨度,单位s
        self.time_span = time_span
        self.exist_movie = True
        self.sleep_time_max = sleep_time_max
        if self.mode == 1:
            # 实时监控某部电影票房就关掉日志
            logger.disable('info')

    def getIndex(self):
        return math.floor(1000 * random.random() + 1)

    def getD(self):
        # d是各种参数的组合,包括timeStamp,User-Agent,index,channelId,sVersion以及key
        self.pay_loads['index'] = self.getIndex()
        self.pay_loads['timeStamp'] = int(time.time() * 1000)
        logger.info('timeStamp:' + str(self.pay_loads['timeStamp']))
        d = 'method=GET&timeStamp=' + str(self.pay_loads['timeStamp']) + '&User-Agent=' + self.pay_loads['User-Agent'] + '&index=' \
            + str(self.pay_loads['index']) + '&channelId=' + str(self.pay_loads['channelId']) + '&sVersion=' + str(self.pay_loads['sVersion']) + \
            '&key=' + self.key
        # 找出目标字符串中的所有空白字符并用空格代替
        d = d.replace(r'/\s+/g'," ")
        return d

    # 得到signKey
    def getSignKey(self):
        md5 = hashlib.md5()
        d = self.getD()
        md5.update(d.encode('utf-8'))
        signKey = md5.hexdigest()
        self.pay_loads['signKey'] = signKey
        logger.info("signKey:" + signKey)

    # 识别数字,因为response里面的票房数据都是字体
    def reconizeNumber(self,font_url):
        """
        识别woff文件里面的数字,将unicode和数字匹配
        :param font_url: 字体网址
        :return:
            font_unicodes:字体对应的unicode编码
            number_list:字体对应的unicode编码所对应的数字
        """
        # SpiderProject.使用cv2识别
        # 2.因为一个只有5个字体文件,可以一一匹配,但比较费时
        # 这里使用第1种
        # 下载字体
        font_resp = requests.get(font_url)
        with open('font.woff','wb') as f:
            f.write(font_resp.content)
            f.close()
        # 以TTF格式打开woff文件
        ttfont = TTFont('font.woff')
        # 按序获取GlyphOrder节点name值
        font_unicodes = ttfont.getGlyphOrder()[2:]
        logger.info('数字对应的unicode:' + str(font_unicodes))
        # 识别数字
        number_list = []
        # 绘制到图像上的字体
        font = ImageFont.truetype("font.woff",40)
        for unicode_font in font_unicodes:
            # 数字内容
            temp = f"\\u{unicode_font[3:]}".encode().decode('unicode_escape')
            # 创建一个Image对象用于存储编码信息
            temp_im = Image.new(mode='RGB',size=(42,40),color='white')
            # 选择绘图的对象
            draw_im = ImageDraw.Draw(im=temp_im)
            # 开始绘图
            draw_im.text(xy=(0,0),text=temp,fill=0,font=font)
            # 得到上面步骤写的二进制数据
            img_byte = io.BytesIO()
            # 保存在Image对象中
            temp_im.save(img_byte,format='JPEG')
            # 进行ocr识别
            number_list.append(self.ocr.classification(img_byte.getvalue()))
        logger.info('unicode对应的字符:' + str(number_list))
        return font_unicodes,number_list

    def unicodeToNum(self,unicode_str,unicodes,number):
        """
        将网页获取的unicode字符串转换成数字
        :param unicode_str: 需要解析的字体字符串
        :param unicodes: 给定的字体对应的unicode编码
        :param number: 给定的字体对应的unicode编码对应的数字
        :return: 解析的数字字符串
        """
        split_unicode = unicode_str.split(';')[:-1]
        split_unicode[-2]=split_unicode[-2][1:]
        # 循环找到数字对应的unicode
        true_num = ""
        for s in range(len(split_unicode)):
            mid = split_unicode[s].replace('&#x','uni')
            for i in range(len(unicodes)):
                if unicodes[i].upper() == mid.upper():
                    if s != len(split_unicode) - 2:
                        relate_num = number[i]
                        true_num = true_num + str(relate_num)
                    else:
                        relate_num = number[i]
                        true_num = true_num + '.' + str(relate_num)
        return true_num

    def getMovieInfo(self,unicodes,number,data):
        movies_info_list = data['movieList']['data']['list']
        movies_info = []

        for movie in movies_info_list:
            name = movie['movieInfo']['movieName']
            release_day = movie['movieInfo']['releaseInfo']
            slice_arr = movie['showCount']
            all_tickets = movie['sumBoxDesc']
            today_ratio = movie['boxRate']
            # 计算当天票房
            today_tickets_str = movie['boxSplitUnit']['num']
            today_tickets = str(self.unicodeToNum(today_tickets_str,unicodes,number)) + '万'
            movie_info = Movie(name,all_tickets,today_tickets,slice_arr,release_day,today_ratio)
            movies_info.append(movie_info)
        return movies_info

    def showMoviesInfo(self,movies_info):
        logger.info('票房信息为:')
        tb = pt.PrettyTable()
        tb.field_names = ["电影名称","综合票房","当日票房","排片数","上映天数","当日票房占比"]
        for movie in movies_info:
            tb.add_row(movie.asList())
        print(tb)

    # 发起请求
    def initialRequest(self):
        # 得到signKey
        self.getSignKey()
        logger.info("发起请求...")
        resp = requests.get(url=self.base_url, headers=self.headers, params=self.pay_loads)
        # print(resp.text)
        resp.encoding = 'utf-8'
        resp_json = resp.json()
        fontStyle = resp_json['fontStyle']
        match_url = 'https:' + re.search(r',url\(".*?.woff', fontStyle)[0][6:]
        logger.info("字体地址:" + match_url)
        # 进行数字的识别
        logger.info("进行数字和unicode编码的匹配...")
        font_unicodes, number_list = self.reconizeNumber(match_url)
        # 获取电影的信息
        logger.info("获取电影的票房信息...")
        movies_info = self.getMovieInfo(font_unicodes, number_list, resp_json)
        return movies_info

    def run(self):
        if self.mode == 0:
            movies_info = self.initialRequest()
            self.showMoviesInfo(movies_info)
        else:
            self.recordSingleMovie()

    # 记录给定电影的单日票房
    def recordSingleMovie(self):
        # 时间
        start_time = int(time.time())
        init_time = start_time
        end_time = start_time + self.time_span
        # 文件名
        file_name = self.movie_name + '.csv'
        exist_file = os.path.exists(file_name)
        while start_time <= end_time:
            movies_info = self.initialRequest()
            # 该电影是否存在
            self.exist_movie = False
            for movie in movies_info:
                if movie.name == self.movie_name:
                    movie_ticket_str = movie.today_tickets
                    self.exist_movie = True
                    break
            if self.exist_movie == False:
                logger.warning("没有找到该电影!")
                break
            cur_time = time.time()
            time_local = time.localtime(int(cur_time))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            # if movie_ticket_str[-SpiderProject] == '万':
            #     movie_ticket = float(movie_ticket_str[:-SpiderProject]) * 10000
            # elif movie_ticket_str[-SpiderProject] == '亿':
            #     movie_ticket = float(movie_ticket_str[:-SpiderProject]) * 100000000
            data_frame = pd.DataFrame({'时间':[dt],'票房':[movie_ticket_str]})
            # 追加到末尾
            if start_time == init_time and exist_file == False:
                add_header = True
            else:
                add_header = False
            data_frame.to_csv(file_name, mode="a", index=False, header=add_header, encoding='gb18030')
            # 休眠
            sleep_time = int(random.random() * (self.sleep_time_max - 20)) + 20
            time.sleep(sleep_time)
            start_time = int(time.time())

    def testMatchFontUrl(self):
        s = '@font-face{font-family: "mtsi-font";src:url("//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/6da1d869.eot");src:url("//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/6da1d869.eot?#iefix") format("embedded-opentype"),url("//s3plus.meituan.net/v1/mss_73a511b8f91f43d0bdae92584ea6330b/font/6da1d869.woff");}'
        print(s)
        match_url = re.search(',url\(".*?.woff', s)
        print(match_url[0])

    def testCountdown(self):
        start_time = int(time.time())
        init_time = start_time
        end_time = start_time + self.time_span
        while start_time <= end_time:
            cur_time = time.time()
            time_local = time.localtime(int(cur_time))
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            data_frame = pd.DataFrame({'时间': [dt], '票房': ["123万"]})
            # 追加到末尾
            if start_time == init_time:
                add_header = True
            else:
                add_header = False
            data_frame.to_csv("test.csv", mode="a", index=False, header=add_header, encoding='gb18030')
            time.sleep(self.sleep_time)
            start_time = int(time.time())


if __name__ == '__main__':
    # 必须知道它的参数怎么来的
    mode = 0
    time_span = 100
    movie_name = "流浪地球2"
    spider = MaoyanMovieSpider(mode=mode,time_span=time_span,name=movie_name)
    # spider.testCountdown()
    # spider.test_match_font_url()
    spider.run()
