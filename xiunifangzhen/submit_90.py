import requests
import json
from loguru import logger
import random
import time
from urllib.parse import quote, unquote

class QiaSumbit():
    def __init__(self,uuid,ticket):
        self.tag = "QiaTongXue"
        # 提交数据的header
        self.submitHeaders = {
          "Accept": "*/*",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
          "Content-Length": "13202",
          "Content-Type": "application/x-www-form-urlencoded",
          "Host": "virtualcourse.zhihuishu.com",
          "Origin": "https://ar.zhihuishu.com",
          "Pragma": "no-cache",
          "Referer": "https://ar.zhihuishu.com/",
          "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-site",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.uuid = uuid
        self.ticket = ticket
        self.file_path = 'static/96_data.json'

        self.other_headers = {
          "Accept": "*/*",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
          "Content-Length": "108",
          "Content-Type": "application/x-www-form-urlencoded",
          "Host": "virtualcourse.zhihuishu.com",
          "Origin": "https://ar.zhihuishu.com",
          "Pragma": "no-cache",
          "Referer": "https://ar.zhihuishu.com/",
          "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-site",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

    def readFromJson(self):
        with open(self.file_path,"r",encoding='utf-8') as f:
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
        ## 3一展厅二、三、四节学习：5    -2
        ## 5二展厅学习：7  -2
        ## 9四展厅学习：11 -2
        ## 11五展厅一、二节学习：5  -1
        ## 13五展厅三、四节学习：3  -1
        ## 15六展厅学习：11    -2
        time_span = [[181,300],[301,500],[301,500],[180,300],[181,300],[301,500]]
        target_score = [5,7,11,5,3,11]
        add = len(target_score) - 1
        for i in range(step_len):
            step = self.data["steps"][step_len - 1 - i]
            # 从一个实验到另外一个实验的时间
            t = random.randint(10, 50)
            all_time_use += t
            k = k - t * 1000
            step["endTime"] = k
            if step['seq'] != 3 and step["seq"] != 5 and step["seq"] != 9 and step['seq'] != 11 and step['seq'] != 13 and step['seq'] != 15:
                # 得到的是当前步骤花费的时间
                t = step["expectTime"] + random.randint(10, 50)
                # 记录使用的时间
                step["timeUsed"] = t
                # 记录当前步骤的分数
                step["score"] = step["maxScore"]
            else:
                t = random.randint(time_span[add][0],time_span[add][1])
                step["timeUsed"] = t
                print(t)
                step["score"] = target_score[add]
                step['evaluation'] = '良'
                # print(step['evaluation'])
                # print(self.data['reportModels'][step_len - 1 - i]['reportContents'][0]['script'])
                self.data['reportModels'][step_len - 1 - i]['reportContents'][0]['script'] = target_score[add]
                add -= 1
            # 增加总共花费的时间
            all_time_use += t
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
    def queryUserInfo(self):
        url = "https://virtualcourse.zhihuishu.com/report/queryIlabUserInfo"
        pay_loads = {
            "appId": "105348",
            "courseId": 2000077162,
            "secret": "bNuKsTVhKwHWL3xzWIfxk1is63VnSfa5sxCnMQDegH0=",
            "ticket": self.ticket
        }
        self.other_headers['Content-Type'] = "application/json"
        self.other_headers['Content-Length'] = "233"
        # 查询信息
        resp = requests.post(url=url,headers=self.other_headers,data=pay_loads)
        logger.info("查询用户的返回信息:" + resp.text)

    def getExperimentTextNew(self):
        url = "https://virtualcourse.zhihuishu.com/report/getExperimentTextNew"
        pay_loads = {
            "experimentId": 473,
            "courseId": 2000077162,
            "fileKey": "恰同学少年证书"
        }
        self.other_headers['Content-Type'] = "application/x-www-form-urlencoded"
        self.other_headers['Content-Length'] = "108"
        resp = requests.post(url=url,headers=self.other_headers,data=pay_loads,timeout=5)
        logger.info("当前接口的返回值:" + resp.text)
        return resp.json()

    def saveExperimentTextNew(self):
        # 先请求getExperimentTextNew
        get_text_resp_json = self.getExperimentTextNew()
        data = get_text_resp_json['data']
        # 然后请求当前的
        url = "https://virtualcourse.zhihuishu.com/report/saveExperimentTextNew"
        pay_loads = {
            "experimentId": 473,
            "courseId": 2000077162,
            "fileKey": "恰同学少年证书",
            "data": int(data) + 1
        }
        self.other_headers['Content-Type'] = "application/x-www-form-urlencoded"
        self.other_headers['Content-Length'] = "120"
        # 使用data可以,但是不能使用params
        resp = requests.post(url=url,headers=self.other_headers,data=pay_loads).text
        logger.info("当前接口的返回值:" + resp)

    def getExpEndTime(self):
        # 获得系统时间的接口
        url = "https://studyservice.zhihuishu.com/api/stuExperiment/systemTime"
        # 请求头部分
        headers = {
          "Accept": "*/*",
          "Accept-Encoding": "gzip, deflate, br",
          "Accept-Language": "zh-CN,zh;q=0.9",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
          "Host": "studyservice.zhihuishu.com",
          "Origin": "https://ar.zhihuishu.com",
          "Pragma": "no-cache",
          "Referer": "https://ar.zhihuishu.com/",
          "sec-ch-ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"Windows\"",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-site",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        # print(headers['sec-ch-ua'])
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
        logger.info("获取用户信息...")
        self.queryUserInfo()
        logger.info("获得并保存证书编号...")
        self.saveExperimentTextNew()
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
        # print(self.data)
        logger.info("提交数据")
        self.submitData()


if __name__ == '__main__':
    # 你的uuid,不需要设置,这个是智慧树那个平台的
    uuid = "Xowq79om"
    # 每个人的是不一样的
    # %3D : =
    # %2F : /
    # %2B : +
    ticket = ""
    ticket = unquote(ticket)
    logger.info('ticket:' + ticket)
    # 你期望的分数,这个要改
    score = 90
    qia = QiaSumbit(uuid,ticket)
    qia.run(score)
    # qia.getExpEndTime()
    # qia.queryUserInfo()
    # qia.saveExperimentTextNew()