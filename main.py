import os
import re
from os import system
from flask import Flask
from requests import *

clashheaders = {
    'User-Agent': 'ClashforWindows/0.20.39'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}

def gethtml():
    try:
        html = get("https://github.com/tolinkshare2/tolinkshare2.github.io/blob/main/README.md", headers=headers,verify=False,proxies = {'http': None,'https': None})
        return html.text
    except Exception as e:
        print(f"请求失败: {e}")
        system("exit")
        return ""

def novpn():
    if 'HTTP_PROXY' in os.environ:
        del os.environ['HTTP_PROXY']
    if 'HTTPS_PROXY' in os.environ:
        del os.environ['HTTPS_PROXY']

def getclash(url):
    try:
        novpn()
        response = get(url, headers=clashheaders,verify=False,proxies = {'http': None,'https': None})
        return response.text
    except RequestException as e:
        print(f"请求失败: {e}")
        return ""

def findhttp(html):
    pattern = r'<code>(.*?)</code>'
    url=re.findall(pattern, html, re.DOTALL)
    url = (url[0])
    url=url[:-1]
    url = url.replace("https://", "http://")
    return url

def startflask():
    app = Flask(__name__)

    @app.route('/')
    def got():
        return main()

    app.run("0.0.0.0", 52025)
def main():
    novpn()
    html=gethtml()
    url=findhttp(html)
    clash=getclash(url)
    return clash

startflask()
# print(main())
