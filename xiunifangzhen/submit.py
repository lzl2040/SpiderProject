import requests
import json
from loguru import logger
import random

class QiaSumbit():
    def __init__(self,uuid,ticket):
        self.tag = "QiaTongXue"
        # 提交数据的header
        self.submitHeaders = {
            "Host": "virtualcourse.zhihuishu.com",
            "Connection": "keep-alive",
            "Content-Length": "23341",
            "sec-ch-ua" : """" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100" """,
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Content-Type":"application/x-www-form-urlencoded",
            "Accept":"*/*",
            "Origin" :"https://ar.zhihuishu.com",
            "Sec-Fetch-Site":"same-site",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Dest":"empty",
            "Referer":"https//ar.zhihuishu.com/",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9 "
        }
        self.uuid = uuid
        self.ticket = ticket

    def readFromJson(self):
        with open("./static/data.json","r",encoding='utf-8') as f:
            data = json.load(f)
        return data

    def modidyExpData(self,endTime,score):
        # 设置实验结束时间
        self.data["endTime"] = endTime
        # 设置实验分数为100
        self.data["score"] = score
        # 总共实验的时间
        all_time_use = 0
        # 记录的其实是最终得到的开始的时间
        k = endTime
        # 总共花的步数
        step_len = len(self.data["steps"])
        # 遍历所有的步数,从结束时间往前推,计算开始时间和每步的时间
        for i in range(step_len):
            step = self.data["steps"][step_len - 1 - i]
            # 从10-50这随机取一个整数，主要是偏移一些时间
            t = random.randint(10, 50)
            all_time_use += t
            k = k - t * 1000
            step["endTime"] = k
            # 得到的是当前步骤花费的时间
            t = step["expectTime"] + random.randint(10, 50)
            # 增加总共花费的时间
            all_time_use += t
            # 记录使用的时间
            step["timeUsed"] = t
            # 记录当前步骤的分数
            step["score"] = step["maxScore"]
            # 往前推时间
            k = k - t * 1000
            # 得到本步开始的时间
            step["startTime"] = k
        # 记录总共花费的时间
        self.data["timeUsed"] = all_time_use
        # 计算开始实验的时间
        start_time = self.data["endTime"] - all_time_use * 1000
        # 记录开始的时间
        self.data["startTime"] = start_time
        self.data['uuid'] = self.uuid

        return json.dumps(self.data)

    def getExpEndTime(self):
        # 获得系统时间的接口
        url = "https://studyservice.zhihuishu.com/api/stuExperiment/systemTime"
        # 请求头部分
        headers = {
            "Host": "studyservice.zhihuishu.com",
            "Connection": "keep-alive",
            "sec-ch-ua": """" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100" """,
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "sec-ch-ua-platform": "Windows",
            "Accept": "*/*",
            "Origin": "https://ar.zhihuishu.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https//ar.zhihuishu.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9 ",
        }
        # 发起请求
        resp = requests.get(url, headers=headers)
        data = resp.text
        data_json = json.loads(data)
        # 返回的是时间戳
        timeStamp = data_json["data"]
        return timeStamp

    def submitData(self):
        # 提交数据的接口
        url = "https://virtualcourse.zhihuishu.com/report/saveReport"
        self.data = {"jsonStr":self.data,"ticket":self.ticket}
        response = requests.post(url, data=self.data, headers=self.submitHeaders)
        logger.info("返回信息为:" + response.text)

    def saveReport(self):
        save_url = "https://service-fhc0s03y-1251776818.gz.apigw.tencentcs.com/release/qtxsn/" + self.uuid
        resp = requests.get(url=save_url)
        logger.info("返回信息为:" + resp.text)

    def run(self,score):
        logger.info("获取实验结束时间...")
        endTime = self.getExpEndTime()
        logger.info("实验结束时间为:" + str(endTime))
        logger.info("读取json数据...")
        self.data = self.readFromJson()
        logger.info("加载json数据完成")
        logger.info("实验ID:" + str(self.data["experimentId"]))
        logger.info("课程ID:" + str(self.data["courseId"]))
        logger.info("修改实验数据...")
        self.data = self.modidyExpData(endTime,score)
        logger.info("提交数据")
        self.submitData()


if __name__ == '__main__':
    # 你的uuid,不需要设置,这个是智慧树那个平台的
    uuid = ""
    # 每个人的是不一样的
    # %3D : =
    # %2F : /
    ticket = ""
    # 你期望的分数
    score = 100
    qia = QiaSumbit(uuid,ticket)
    # qia.saveReport()
    qia.run(score)