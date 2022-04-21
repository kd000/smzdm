"""
什么值得买自动签到脚本

借鉴（copy）自lws1122,fork 自:https://gitee.com/lsw1122/smzdm_bot
"""
'''
cron: 0 1 * * * smzdm.py
new Env('张大妈自动签到');
'''

import requests, os, datetime, sys
from sys import argv
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
#from checksendNotify import send
from notify import send
"""
http headers
"""
DEFAULT_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'zhiyou.smzdm.com',
    'Referer': 'https://www.smzdm.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}

# 签到用的url
SIGN_URL = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
#SIGN_URL = 'https://zhiyou.smzdm.com/user/info/jsonp_get_current'

# 环境变量中用于存放cookie的key值
KEY_OF_COOKIE = "SMZDM_COOKIE"

TG_TOKEN = ''
TG_USER_ID = ''
# serverJ
SCKEY = ''
# push+
PUSH_PLUS_TOKEN = ''
# 钉钉机器人
DD_BOT_TOKEN = ''
DD_BOT_SECRET = ''

if "TG_BOT_TOKEN" in os.environ and len(os.environ["TG_BOT_TOKEN"]) > 1 and "TG_USER_ID" in os.environ and len(
        os.environ["TG_USER_ID"]) > 1:
    TG_TOKEN = os.environ["TG_BOT_TOKEN"]
    TG_USER_ID = os.environ["TG_USER_ID"]

if "PUSH_KEY" in os.environ and len(os.environ["PUSH_KEY"]) > 1:
    SCKEY = os.environ["PUSH_KEY"]

if "DD_BOT_TOKEN" in os.environ and len(os.environ["DD_BOT_TOKEN"]) > 1 and "DD_BOT_SECRET" in os.environ and len(
        os.environ["DD_BOT_SECRET"]) > 1:
    DD_BOT_TOKEN = os.environ["DD_BOT_TOKEN"]
    DD_BOT_SECRET = os.environ["DD_BOT_SECRET"]

if "PUSH_PLUS_TOKEN" in os.environ and len(os.environ["PUSH_PLUS_TOKEN"]) > 1:
    PUSH_PLUS_TOKEN = os.environ["PUSH_PLUS_TOKEN"]


def logout(self):
    print("[{0}]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self))
    sys.stdout.flush()


class SignBot(object):

    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            return True
        except Exception as e:
            logout(f'Error : {e}')
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies

    def checkin(self):
        """
        签到函数
        """
        msg = self.session.get(SIGN_URL)
        if self.__json_check(msg):
            return msg.json()
        return msg.content


if __name__ == '__main__':
    bot = SignBot()
    cookies = os.environ[KEY_OF_COOKIE]
    cookieList = cookies.split("&")
    logout("检测到{}个cookie记录\n开始签到".format(len(cookieList)))
    index = 0
    for c in cookieList:
        bot.load_cookie_str(c)
        result = bot.checkin()
        msg = "\n⭐⭐⭐签到成功{1}天⭐⭐⭐\n🏅🏅🏅金币[{2}]\n🏅🏅🏅积分[{3}]\n🏅🏅🏅经验[{4}],\n🏅🏅🏅等级[{5}]\n🏅🏅补签卡[{6}]".format(
            index,
            result['data']["checkin_num"],
            result['data']["gold"],
            result['data']["point"],
            result['data']["exp"],
            result['data']["rank"],
            #result['data']["silver"],
            #result['data']["prestige"],
            result['data']["cards"])
        logout(msg)
        logout("开始推送")
        # telegram_bot("张大妈自动签到", msg)
        index += 1
    logout("签到结束")
    send('张大妈自动签到',msg)
