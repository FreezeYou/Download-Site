#!/usr/bin/python3
import os
import urllib.parse

import requests
import wget

if os.path.exists("syncing.lock"):
    print("另一个同步正在进行")
    exit()

os.mknod("syncing.lock")

dataJson = requests.get("https://api.github.com/repos/FreezeYou/FreezeYou/releases").json()

print("正在同步...")

for releaseData in dataJson:
    fileName: str = urllib.parse.unquote(releaseData["name"])
    downloadUrl: str = urllib.parse.unquote(releaseData["assets"][0]["browser_download_url"])
    if fileName is not None or downloadUrl is not None:
        if not os.path.exists(fileName + ".apk"):
            print("正在下载：" + downloadUrl)
            wget.download(downloadUrl, fileName + ".apk")
            print("\r\n同步 " + fileName + " 完成")
        else:
            print("已存在的：" + fileName + ".apk")
    else:
        print("\r\n同步 " + str(fileName) + " 失败")

os.remove("syncing.lock")

print("同步完成")
