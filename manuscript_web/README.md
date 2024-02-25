# 自动检测IEEE Manuscript网站论文状态
## 前言
众所周知，IEEE的期刊审核是十分慢的，而每天去官网看投稿状态的变化是一件极其分神的事情，因此使用脚本来自动检测投稿状态的变化是十分有必要的。
## 步骤
只需简单的几个步骤，即可让你省去查看投稿状态的时间，能够使用的前提为：
- 你需要有两个邮箱，一个用于发送邮件（最好是163邮箱），一共用于接收邮箱

具体步骤为： 
- 开启用于发送邮件的邮箱的POP3/SMTP服务

    服务的开启见此链接：[python自动发送邮件](https://blog.csdn.net/c1007857613/article/details/129751652)
- 获得获取对应邮箱的SMTP授权码，填入代码中的```auth_key```
- ```sender_email```填发送邮件的邮箱地址，```receiver_email```填接收邮件的邮箱地址
- 根据自己的需要修改```trans_type```，注意，需要先看官网的网址，如：

    若网址为https://mc.manuscriptcentral.com/tpami-cs，则```trans_type="tpami-cs"```，而不是```tpami```。
- 最后运行即可，如果有服务器的话，可以挂在服务器上后台运行。
## 遇到的问题
### The chromedriver version cannot be discovered
没有找到浏览器驱动

解决办法：使用chrome_driver_path指定路径

```
from splinter import Browser
chrome_driver_path = "path"
b = Browser('chrome', headless=True, executable_path=chrome_driver_path)
```
### element click intercepted: Element is not clickable at point
网速问题，页面还没加载出来
