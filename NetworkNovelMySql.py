import requests  # 获取网页信息
from bs4 import BeautifulSoup as BS  # 解析网页，比正则表达式好用太多了
import time
import datetime
from MysqlHelper import MysqlHelper
import config

file_num = 0  # 下载文件数目
file_list_url = []  # 下载的url
file_list_name = []  # 下载的名字
book_name = ''

# 模拟浏览器发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


# 下载小说章节信息
def download(book_name):
    # 获取小说库里存的ID
    query_params = [book_name]
    bookId = MysqlHelper.query_one(config.QUERY_ID_BY_BOOKNAME_SQL, query_params)
    print("开始下载章节内容.....")
    cu_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_batch_params = []
    for i in range(file_num):
        target = file_list_url[i]  # 获取下载地址
        r = requests.get(target, headers=headers)
        html = r.text  # 得到html
        bf = BS(html, "lxml")
        texts = bf.find_all('div', class_='content', itemprop='acticleBody')  # 寻找正文部分
        ac = []
        insert_params = []
        for k in range(len(texts[0].contents)):
            tmp = str(texts[0].contents[k]).replace("</p>", "\n")
            ac.append(tmp.replace("<p>", ""))
        insert_params.append(bookId[0])
        insert_params.append(str(file_list_name[i]))
        insert_params.append("".join(ac))
        insert_params.append(0)
        insert_params.append(i + 1)
        insert_params.append('admin')
        insert_params.append(cu_time)
        insert_params.append(cu_time)
        insert_params.append('admin')
        insert_batch_params.append(insert_params)
        time.sleep(3)  # 等待3s，防止出现验证码
        print("已爬取第" + str(i + 1) + "章节内容！")
        if len(insert_batch_params) >= 20:
            MysqlHelper.insert_batch(config.INSERT_BATCH_CHAPTER_SQL, insert_batch_params)
            insert_batch_params = []
            print("已存入" + str(i + 1) + "章节")
    if len(insert_batch_params) > 0:
        MysqlHelper.insert_batch(config.INSERT_BATCH_CHAPTER_SQL, insert_batch_params)
        print("已存入" + str(file_num) + "章节")


# 获取目录信息方法
def get_list(url):
    r = requests.get(url, headers=headers)
    html = r.text
    bf = BS(html, "lxml")
    # 获取小说名称
    title = bf.find_all('div', class_='book-meta')
    title_bf = BS(str(title[0]), "lxml")
    title = title_bf.find_all('h1')
    for tit in title:
        global book_name
        book_name = str(tit.text)
    # 获取小说目录列表
    texts = bf.find_all('div', class_='volume-list')
    bf = BS(str(texts[0]), "lxml")
    texts = bf.find_all('a')  # 从标题列表中筛选出需要的
    for ac in texts:
        if (str(ac.text) == "[分卷阅读]"):  # 除去目录中无用的url
            continue
        file_list_url.append(ac.attrs['href'])  # 存入下载地址
        file_list_name.append(str(ac.text))  # 存入小说名
        global file_num  # 全局变量必须在函数内部说明 使用 global
        file_num = file_num + 1  # 下载数目
    print("获得目录数量：" + str(file_num))


url = "http://book.zongheng.com/showchapter/992851.html"  # 需要填写的目录列表
if __name__ == '__main__':
    print("------小说下载开始------")
    get_list(url)  # 下载目录
    download(book_name)  # 下载章节
    print("\n------小说下载完成------")
