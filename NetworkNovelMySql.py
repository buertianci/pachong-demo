import requests  # 获取网页信息
from bs4 import BeautifulSoup as BS  # 解析网页，比正则表达式好用太多了
import time
import datetime
from MysqlHelper import MysqlHelper
import config

file_num = 0  # 下载文件数目
file_list_url = []  # 下载的url
file_list_name = []  # 下载的名字
book_id = 0  # 书ID
book_list_url = ''  # 书章节URL
author_id = 0  # 作者信息id
author_name = ''  # 作者名称

# 模拟浏览器发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


# 由于该爬虫最初是给库里存在的书爬取内容的，所以未对书内容是否已存在做校验
# 后期可以优化对连载小说增量更新内容
# 下载小说章节信息
def go_download_chapter():
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
        insert_params.append(book_id)
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
def get_book_list(book_list_url):
    r = requests.get(book_list_url, headers=headers)
    html = r.text
    bf = BS(html, "lxml")
    # 获取小说目录列表
    texts = bf.find_all('div', class_='volume-list')
    bf = BS(str(texts[0]), "lxml")
    texts = bf.find_all('a')  # 从标题列表中筛选出需要的
    for ac in texts:
        if str(ac.text) == "[分卷阅读]":  # 除去目录中无用的url
            continue
        file_list_url.append(ac.attrs['href'])  # 存入下载地址
        file_list_name.append(str(ac.text))  # 存入小说名
        global file_num  # 全局变量必须在函数内部说明 使用 global
        file_num = file_num + 1  # 下载数目
    print("获得目录数量：" + str(file_num))


# 获取书的基本信息
def get_book_info(book_info_url):
    cu_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 作者id, 分类, 频道
    insert_book_params = [author_id, 1100, 1]
    global book_id
    r = requests.get(book_info_url, headers=headers)
    html = r.text
    bf = BS(html, "lxml")
    lists = bf.find_all('div', class_='book-label')
    lists_bf = BS(str(lists[0]), "lxml")
    lists = lists_bf.find_all('a')
    # 连载状态
    if str(lists[0].text) == '已完结':
        insert_book_params.append(3)
    elif str(lists[0].text) == '连载中':
        insert_book_params.append(1)
    else:
        insert_book_params.append(2)
    # 书状态-默认上架
    insert_book_params.append(1)
    book_url_str = book_info_url.split("/")
    length = len(book_url_str)
    # 书ID
    insert_book_params.append(str(book_url_str[length - 1].split(".")[0]))
    # 书名
    lists = bf.find_all('div', class_='book-name')
    book_name = str(lists[0].text)
    insert_book_params.append(book_name.strip())
    # 校验该书是否存在
    res = MysqlHelper.query_one(config.QUERY_BOOK_ID_SQL, book_name.strip())
    if res is not None:
        book_id = res[0]
        print("库里已经存在该书信息！")
        return
    # 书评分
    insert_book_params.append(4)
    key_word_sp = lists_bf.find_all('span')
    key_word_bf = BS(str(key_word_sp[0]), "lxml")
    key_word_lists = key_word_bf.find_all('a')
    key_word_str = ''
    for key_word in key_word_lists:
        key_word_str = key_word_str + " " + key_word.text
    # 书-关键字
    insert_book_params.append(key_word_str)
    # 获取书图片URL
    book_img_div = bf.find_all('div', class_='book-img fl')
    book_img_bf = BS(str(book_img_div[0]), "lxml")
    book_imgs = book_img_bf.find_all('img')
    for book_img in book_imgs:
        insert_book_params.append(book_img.attrs['src'])
    # 作者名称
    insert_book_params.append(author_name)
    # 书简介
    book_intro_div = bf.find_all('div', class_='book-dec Jbook-dec hide')
    book_intro_bf = BS(str(book_intro_div[0]), "lxml")
    book_intros = book_intro_bf.find_all('p')
    book_intro = str(book_intros[0])
    # 书简介
    insert_book_params.append(book_intro.replace('<p>', '').replace('</p>', '').replace('<br/>', '\n'))
    # 字数
    book_num_div = bf.find_all('div', class_='nums')
    book_num_bf = BS(str(book_num_div[0]), "lxml")
    book_nums = book_num_bf.find_all('i')
    book_num = str(book_nums[0].text)
    numeric = '0123456789-.'
    for i, c in enumerate(book_num):
        if c not in numeric:
            break
    number = float(book_num[:i])
    unit = book_num[i:].strip()
    if unit == '万':
        number = number * 10000
    elif unit == '亿':
        number = number * 100000000
    # 书字数
    insert_book_params.append(int(number))
    insert_book_params.append("admin")
    insert_book_params.append(cu_time)
    insert_book_params.append(cu_time)
    insert_book_params.append("admin")
    # 将书基本信息存入表
    book_id = MysqlHelper.insert_one(config.INSERT_BOOK_INFO_SQL, insert_book_params)
    print("书基本信息存入库。。。")


# 获取作者的基本信息
def get_author_info(book_info_url):
    cu_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 作者信息参数变量
    insert_author_params = []
    global author_id
    r = requests.get(book_info_url, headers=headers)
    html = r.text
    bf = BS(html, "lxml")
    # 获取目录链接
    lists = bf.find_all('div', class_='fr link-group')
    lists_bf = BS(str(lists[0]), "lxml")
    lists = lists_bf.find_all('a')
    global book_list_url
    book_list_url = lists[0].attrs['href']
    # 获取作者名称 详情链接
    author = bf.find_all('div', class_='au-name')
    author_bf = BS(str(author[0]), "lxml")
    author = author_bf.find_all('a')
    author_href = ''
    for au in author:
        author_href = au.attrs['href']
        global author_name
        author_name = au.text
        insert_author_params.append(author_name)
    # 校验该作者是否已经存在库中
    res = MysqlHelper.query_one(config.QUERY_AUTHOR_ID_SQL, author_name)
    if res is not None:
        author_id = res[0]
        print("库里已经存在该作者信息！")
        return
    # 通过作者详情链接获取作者其他信息
    r = requests.get(author_href, headers=headers)
    html = r.text
    bf = BS(html, "lxml")
    # 作者简介
    auth_intro = bf.find_all('p', class_='intro')
    for auth_in in auth_intro:
        insert_author_params.append(auth_in.text)
    # 头像图片地址
    auth_imgs = bf.find_all('div', class_='user-head')
    auth_imgs_bf = BS(str(auth_imgs[0]), "lxml")
    auth_imgs = auth_imgs_bf.find_all('img')
    for au_img in auth_imgs:
        insert_author_params.append(au_img.attrs['src'])
    insert_author_params.append("admin")
    insert_author_params.append(cu_time)
    insert_author_params.append(cu_time)
    insert_author_params.append("admin")
    # 存储作者信息到mysql中
    author_id = MysqlHelper.insert_one(config.INSERT_AUTHOR_INFO_SQL, insert_author_params)
    print("作者信息存入库。。。")


book_info_url = "http://book.zongheng.com/book/1072307.html"
if __name__ == '__main__':
    print("------小说下载开始------")
    get_author_info(book_info_url)  # 获取作者信息
    get_book_info(book_info_url)  # 获取书基本信息
    get_book_list(book_list_url)  # 下载目录
    go_download_chapter()  # 下载章节
    print("\n------小说下载完成------")
