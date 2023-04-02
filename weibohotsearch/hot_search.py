import requests
from loguru import logger
import json
import time
from connection import MysqlConnection
import prettytable as pt

class HotBand():
    def __init__(self,note,categoty,num,date,url,rank,raw_hot):
        self.note = note
        self.category = categoty
        self.num = num
        self.date = date
        self.url = url
        self.rank = rank
        self.raw_hot = raw_hot

    def asList(self):
        return [self.rank,self.date,self.category,self.note,self.num,self.url]

class HotSearch():
    def __init__(self,url):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"
        }
        self.url = url
        # 查询热搜的网址
        self.query_base_url = "https://s.weibo.com/weibo?q="
        self.connection = MysqlConnection(name='root', pwd="123456", host='localhost', db_name='test').connect()
        # print(self.connection)
        self.conn_status = self.judgeConnection(self.connection)
        self.cursor = None

    def judgeConnection(self, conn):
        if conn == None:
            logger.warning("数据库连接失败")
            return False
        else:
            logger.info("数据库连接成功")
            # print(self.cursor)
            return True

    def timeStampToDate(self,time_stamp):
        time_array = time.localtime(time_stamp)
        date_str = time.strftime("%Y-%m-%d %H:%M", time_array)
        return date_str

    def getHotContent(self,json_str):
        # 获得政府相关热搜
        hot_gov_content = json_str['hotgov']['name'].split("#")[1]
        hot_gov_url = json_str['hotgov']['url']
        logger.info("政府相关热搜为:" + hot_gov_content + " 网址为:" + hot_gov_url)
        # 获得实时热搜前50条
        realtime_lists = json_str['realtime']
        hot_bands = []
        for band in realtime_lists:
            # 内容
            note = band['note']
            # 分类
            category = band['category']
            # 当前热度
            hot_num = band['num']
            # 原始热度
            hot_raw_num = band['raw_hot']
            # 上榜时间
            hot_time_stamp = band['onboard_time']
            hot_date = self.timeStampToDate(hot_time_stamp)
            # 查询网址
            hot_query_url = self.query_base_url + "%23" + note + "%23"
            # 排名
            hot_rank = band['rank']
            my_band = HotBand(note,category,hot_num,hot_date,hot_query_url,hot_rank + 1,hot_raw_num)
            hot_bands.append(my_band)
        return hot_bands

    def showBandInfo(self,hot_bands):
        # 先删除之前存储的50条数据
        self.deleteFirst50()
        # 展示并保存当前的数据
        logger.info("热搜信息为:")
        tb = pt.PrettyTable()
        tb.field_names = ["热搜排名","上榜时间", "热点分类", "内容", "当前热度", "热搜网址"]
        for band in hot_bands:
            tb.add_row(band.asList())
            # 保存到数据库中
            if self.conn_status:
                self.saveIntoDataBase(band)
        # 关闭cursor对象
        self.cursor.close()
        # 关闭connection对象
        self.connection.close()
        print(tb)

    def saveIntoDataBase(self,hot_band):
        self.cursor = self.connection.cursor()
        # sql语句
        sql = "insert into hotband(rank,date,category,note,num,url) values(%s,%s,%s,%s,%s,%s)"
        try:
            # 执行sql语句
            self.cursor.execute(sql,hot_band.asList())
            # 提交这个事务
            self.connection.commit()
        except:
            self.connection.rollback()
    def deleteFirst50(self):
        self.cursor = self.connection.cursor()
        # 删除前50条数据
        sql = "delete from hotband order by item_id limit 50"
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交这个事务
            self.connection.commit()
        except:
            self.connection.rollback()


    def run(self):
        logger.info("发起请求")
        resp = requests.get(url=self.url,headers=self.headers)
        logger.info("解析json数据")
        resp.encoding = 'utf-8'
        json_str = resp.json()
        logger.info("获得json数据")
        hot_bands = self.getHotContent(json_str['data'])
        logger.info("展示并保存数据")
        self.showBandInfo(hot_bands)

if __name__ == '__main__':
    url = "https://weibo.com/ajax/side/hotSearch"
    hot = HotSearch(url)
    hot.run()
