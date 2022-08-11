import requests
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import urllib.request
import os

# ---------------------------------------------- #

# 爬取的地址
init_path = "http://116.204.156.73:7772/plate/"

# 爬取文件的存储路径
save_path = "D:/chat_videos/"

# Headers-UserAgent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 " \
             "Safari/537.36 "

# ---------------------------------------------- #

# -------------------系统变量--------------------- #

# 获取etree
etree = html.etree

# -------------------系统变量--------------------- #


# 根据URL获取该URL中所有的A链接的href属性的值
def getXpathByPath(path):
    v = requests.get(url=path, headers={"UserAgent":user_agent}).text
    # 获取xpath对象
    html = etree.HTML(v)
    aList = html.xpath("/html//a/@href")
    result = ""
    for a in aList:
        # 过滤掉每个返回上层级目录的按钮
        if a == "../":
            continue
        if a.endswith("/"):
            getXpathByPath(path + a)
        else:
            result = path + a
            temp_path = path.replace(init_path, "")
            if not os.path.exists(save_path + temp_path):
                os.makedirs(save_path + temp_path)
            with open(save_path + temp_path + a, 'wb') as writer:
                writer.write(urllib.request.urlopen(result).read())
            print(result + " downloading...")
    return result


# 入口函数
if __name__ == '__main__':
    aList = getXpathByPath(init_path)

