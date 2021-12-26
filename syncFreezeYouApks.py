#!/usr/bin/python3
import os
import signal
import urllib.parse
import time

import requests
import wget


def print_log(log, category="INFO", style="0;30"):
    print("\033[{0}m{1} [{2}] {3}\033[0m".format(
        style, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), category, log))


def cleanup(signum, frame):
    if os.path.exists("syncing.lock"):
        os.remove("syncing.lock")
    print_log("Bye~")
    exit()


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if os.path.exists("syncing.lock"):
    print_log("另一个同步正在进行", "WARN", "0;33")
    exit()

os.mknod("syncing.lock")

print_log("正在同步...")

dataJson = requests.get("https://api.github.com/repos/FreezeYou/FreezeYou/releases").json()

for releaseData in dataJson:
    fileName: str = urllib.parse.unquote(releaseData["name"])
    downloadUrl: str = urllib.parse.unquote(releaseData["assets"][0]["browser_download_url"])
    if fileName is not None and downloadUrl is not None:
        if not os.path.exists(fileName + ".apk"):
            print_log("正在下载：" + downloadUrl)
            wget.download(downloadUrl, fileName + ".apk")
            print("\r\n")
            print_log("同步 " + fileName + " 完成")
        else:
            print_log("已存在的：" + fileName + ".apk")
    else:
        print("\r\n")
        print_log("有一项同步失败")

os.remove("syncing.lock")

print_log("同步完成")
