import json
import execjs
import requests
# pip install PyExecJS
from loguru import logger

if __name__ == '__main__':
    # 获取评论
    get_comment_url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
    }
    '''
        rid:前面的部分是固定的,472603422其实为歌曲的id
        pageNo:当前的页数
        pageSize:当前一页展示的评论数目
        orderType:获取的评论类型
    '''
    data = {
        "rid":"R_SO_4_472603422",
        "threadId":"R_SO_4_472603422",
        "pageNo":"1",
        "pageSize":"20",
        "cursor":"-1",
        "offset":"0",
        "orderType":"1",
        "csrf_token":""
    }

    # 转换为json字符串
    json_string = json.dumps(data)
    # 调用json文件
    logger.info('获取加密参数中...')
    ctx = execjs.compile(open('encry.js', 'r', encoding='utf-8').read()).call('d', json_string)
    logger.info('加密的参数为:')
    print(ctx)
    # 组成提交的数据
    post_data = {}
    post_data['params'] = ctx['encText']
    post_data['encSecKey'] = ctx['encSecKey']
    # print(post_data)
    response = requests.post(url=get_comment_url,data=post_data)
    # print(response.text)
    response.encoding = 'utf-8'
    json_resp = response.json()
    # print(json_resp)
    comments = json_resp['data']['comments']
    total_comment_num = json_resp['data']['totalCount']
    logger.info("总评论数为:" + str(total_comment_num))
    logger.info("相关评论内容:")
    for comment in comments:
        content = comment['content']
        print(content)
    # print(data['rid'])
