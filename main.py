import requests
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import urllib.request
import os

# ---------------------------------------------- #

# 爬取的地址
init_path = "http://116.204.156.73:7772/plate/"

# 爬取文件的存储路径
save_path = "D:/chat_videos2/"

# Headers-UserAgent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 " \
             "Safari/537.36 "

# 线程数量
thread_count = 10
# ---------------------------------------------- #

# -------------------系统变量--------------------- #

# 获取etree
etree = html.etree

# -------------------系统变量--------------------- #


# 根据路径获取所有的子目录
def find_child_path_by_path(path):
    v = requests.get(url=path, headers={"UserAgent": user_agent}).text
    # 获取xpath对象
    html = etree.HTML(v)
    a_list = html.xpath("/html//a/@href")
    a_list.remove("../")
    return a_list


# 子目录不单独起线程
def start_child(path):
    a_list = find_child_path_by_path(path)
    for a in a_list:
        try_downloading_file(path, a)


# 尝试下载文件
# 如果path参数以/结尾，则表示是一个子目录，继续递归。
# 如果path参数非/结尾，则执行下载
def try_downloading_file(path, a):
    # 过滤掉每个返回上层级目录的按钮
    if a.endswith("/"):
        start_child(path + a)
    else:
        # 下载路径
        downloading_path = path + a
        # 含有目录的存储路径
        real_save_path = save_path + path.replace(init_path, "")
        if not os.path.exists(real_save_path):
            os.makedirs(real_save_path)
        with open(real_save_path + a, 'wb') as writer:
            writer.write(urllib.request.urlopen(downloading_path).read())
            print(downloading_path + " downloading...")


# 获取多个模块的目录，每个模块使用单独的线程处理
def start_main(path):
    a_list = find_child_path_by_path(path)
    # 使用线程池处理下载
    with ThreadPoolExecutor(thread_count) as t:
        for a in a_list:
            t.submit(try_downloading_file, path, a)


# 入口函数
if __name__ == '__main__':
    start_main(init_path)

