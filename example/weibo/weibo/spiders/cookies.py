# encoding=utf-8
import json
import base64
import requests
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream = logging.StreamHandler()
logger.addHandler(stream)


def getCookies(username, password):
    """ 获取微博Cookies """
    cookie = None
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        logger.info("Get Cookie Success!( username:%s )" % username)
        cookie = session.cookies.get_dict()
    else:
        logger.warn("Failed!( Reason:%s )" % info['reason'])
    return cookie


if __name__ == "__main__":
    auth = ('shudieful3618@163.com','a123456')
    cookie = getCookies(*auth)
    if cookie:
        print "Get Cookies Finish!( Num:%d)" % len(cookie)
