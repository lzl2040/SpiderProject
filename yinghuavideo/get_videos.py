import requests
import re
from bs4 import BeautifulSoup
from loguru import logger
# 多线程
import aiohttp
import aiofiles
import asyncio
import os

class YinghuaCD():
    def __init__(self,url):
        self.url = url
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
        }
        self.iframe_base_url = "https://tup.yinghuacd.com/?vid="
        self.video_desc = ""
        # m3u8保存的地址
        self.m3u8_save_path = "./video/m3u8/"
        # ts文件保存的地址
        self.ts_save_path = "./video/ts/"
        # video保存的地址
        self.video_save_path = "./video/"

    def getIframeUrl(self):
        """
        得到iframe标签的地址
        :return: 返回地址
        """
        resp = requests.get(self.url,headers=self.headers)
        # 返回的网页会乱码,需要将编码改成utf-8
        resp.encoding = 'utf-8'
        # 而且由于界面中含有iframe元素,请求url是返回不了里面的内容的
        # 首先找到iframe的地址
        sp = BeautifulSoup(resp.text,'html.parser')
        data_vid = sp.find(id='playbox')['data-vid']
        iframe_url = self.iframe_base_url + data_vid
        logger.info('iframe url:' + iframe_url)
        # 获得视频(动漫,电视剧名字)
        # SpiderProject.使用meta标签获取
        # self.video_name = sp.find(attrs={"name":"keywords"})['content']
        # 2.使用title获取
        self.video_desc = sp.find('title').text.split('—')[0]
        logger.info("视频名称:" + str(self.video_desc))
        self.video_save_path += (self.video_desc + ".mp4")
        return iframe_url

    def getM3u8Url(self,iframe_url):
        """
        得到m3u8文件的地址
        :param iframe_url: iframe所处的地址
        :return: 返回m3u8的地址
        """
        resp = requests.get(url=iframe_url, headers=self.headers)
        # 用于提取m3u8地址
        obj = re.compile(r"url: \"(?P<url>.*?)\",", re.S)
        m3u8_url = obj.search(resp.text).group("url")
        logger.info("m3u8 url:" + m3u8_url)
        return m3u8_url

    def downloadM3u8(self,m3u8_url):
        """
        下载m3u8文件
        :param m3u8_url: m3u8文件的网址
        """
        logger.info("m3u8文件下载中...")
        # 获得m3u8文件名称
        self.m3u8_save_path += (self.video_desc + ".m3u8")
        # 发起请求
        resp = requests.get(url=m3u8_url,headers=self.headers)
        with open(self.m3u8_save_path,mode='wb') as f:
            f.write(resp.content)
        resp.close()
        logger.info('m3u8文件下载完毕')

    async def download_ts(self,ts_url,ts_name,session):
        """
        异步下载ts文件子任务
        :param ts_url: ts文件地址
        :param ts_name: ts文件名称
        :param session: 开启的会话
        """
        async with session.get(ts_url,headers=self.headers) as resp:
            async with aiofiles.open(self.ts_save_path + ts_name,mode='wb') as f:
                await f.write(await resp.content.read())
        logger.info(f'下载{ts_name}完毕')

    async def aioLoadM3u8(self,m3u8_path):
        """
        使用异步操作下载m3u8文件中的ts文件
        :param m3u8_path: m3u8文件保存的地址
        """
        tasks = []
        n = 0
        # 提前准备好session
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(m3u8_path,mode='r',encoding='utf-8') as f:
                async for line in f:
                    if line.startswith('#') or n > 20:
                        continue
                    # ts文件
                    # 去掉空格和换行
                    line = line.strip()
                    ts_name = line.split('/')[-1]
                    # 创建任务
                    task = asyncio.create_task(self.download_ts(line,ts_name,session))
                    tasks.append(task)
                    n += 1
                # 等待任务结束
                await asyncio.wait(tasks)

    def mergeTs(self,m3u8_path,save_path):
        """
        合并ts文件
        :param m3u8_path: m3u8文件的路径
        :param save_path: 视频保存的路径
        """
        logger.info("拼接ts文件...")
        n = 0
        # 先创建一个mp4文件,然后将ts文件内容写入其中
        with open(save_path,mode='wb') as s:
            with open(m3u8_path,mode='r',encoding='utf-8') as f:
                for line in f:
                    if line.startswith('#') or n > 20:
                        continue
                    line = line.strip()
                    ts_name = line.split('/')[-1]
                    with open(self.ts_save_path + ts_name,mode='rb') as t:
                        s.write(t.read())
                    n += 1
        # 合并ts为mp4文件
        logger.info(f"{self.video_desc}.mp4拼接完成")

    def loadM3u8FileWOMThread(self,m3u8_path):
        """
        没有使用异步操作下载m3u8文件中的ts文件
        :param m3u8_path: m3u8文件保存的地址
        """
        n = 0
        with open(m3u8_path,mode="r") as f:
            for line in f:
                # 去除空格
                line = line.strip()
                if line.startswith("#"):
                    # #开头的不需要
                    continue
                resp = requests.get(line,headers=self.headers)
                with open(f"./video/ts/{n}.ts",mode='wb') as f2:
                    f2.write(resp.content)
                resp.close()
                n += 1

    def run(self):
        # SpiderProject.获得iframe地址
        iframe_url = self.getIframeUrl()
        # 2.获得m3u8地址
        m3u8_url = self.getM3u8Url(iframe_url)
        # 3.下载m3u8文件
        self.downloadM3u8(m3u8_url)
        # 4.异步下载ts文件
        # 这样就不会出现RuntimeError:Event loop is closed这个错误了
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.aioLoadM3u8(m3u8_path=self.m3u8_save_path))
        # 5.合并ts文件
        self.mergeTs(m3u8_path=self.m3u8_save_path,save_path=self.video_save_path)


if __name__ == '__main__':
    url = "http://www.yinghuacd.com/v/5835-8.html"
    yinghua = YinghuaCD(url=url)
    yinghua.run()