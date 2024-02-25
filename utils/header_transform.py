from lxpy import copy_headers_dict

if __name__ == '__main__':
    headers = """
    Accept: */*
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: no-cache
    Connection: keep-alive
    Host: studyservice.zhihuishu.com
    Origin: https://ar.zhihuishu.com
    Pragma: no-cache
    Referer: https://ar.zhihuishu.com/
    sec-ch-ua: "Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-site
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
    """
    headers = copy_headers_dict(headers)
    print(headers)
