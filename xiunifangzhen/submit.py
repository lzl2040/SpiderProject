import requests
import json
from loguru import logger
import random

class QiaSumbit():
    def __init__(self):
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
        # 记录结束的
        k = endTime
        # 总共花的步数
        step_len = len(self.data["steps"])
        # 遍历所有的步数
        for i in range(step_len):
            step = self.data["steps"][step_len - 1 - i]
            t = random.randint(4, 50)  # 未在17个模块中花费的时间
            all_time_use += t
            k = k - t * 1000
            step["endTime"] = k

            t = step["expectTime"] + random.randint(4, 50)
            all_time_use += t
            step["timeUsed"] = t
            step["score"] = step["maxScore"]
            k = k - t * 1000
            step["startTime"] = k
        # 记录总共花费的时间
        self.data["timeUsed"] = all_time_use
        # 计算开始实验的时间
        start_time = self.data["endTime"] - all_time_use * 1000
        self.data["startTime"] = start_time
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
        self.data = {"jsonStr":self.data,"ticket":None}
        response = requests.post(url, data=self.data, headers=self.submitHeaders)
        logger.info("返回信息为:" + response.text)

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
    # 你期望的分数
    score = 100
    qia = QiaSumbit()
    qia.run(score)