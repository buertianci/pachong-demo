import requests
from bs4 import BeautifulSoup as BS  # 解析网页，比正则表达式好用太多了
import time  # 定时

file_num = 0  # 下载文件数目
file_list_url = []  # 下载的url
file_list_name = []  # 下载的名字

# 模拟浏览器发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}


# 下载小说章节信息
def download():
    print("开始下载章节内容.....")
    for i in range(file_num):
        target = file_list_url[i]  # 获取下载地址
        r = requests.get(target, headers=headers)
        html = r.text  # 得到html
        bf = BS(html, "lxml")
        texts = bf.find_all('div', class_='content', itemprop='acticleBody')  # 寻找正文部分
        ac = []
        for k in range(len(texts[0].contents)):
            tmp = str(texts[0].contents[k]).replace("</p>", "\n")
            ac.append(tmp.replace("<p>", ""))
        # ac= texts[0].text.replace("。","。\n")            #切割换行
        write_text(str(file_list_name[i] + ".txt"), ac)  # 写入
        time.sleep(3)  # 等待3s，防止出现验证码
        print("已完成" + str(i + 1) + "部章节")


# 获取目录信息方法
def get_list(url):
    r = requests.get(url, headers=headers)
    html = r.text
    bf = BS(html, "lxml")
    texts = bf.find_all('div', class_='volume-list')  # 获取标题的列表
    bf = BS(str(texts[0]), "lxml")
    texts = bf.find_all('a')  # 从标题列表中筛选出需要的
    file = []  # 标题列表
    for ac in texts:
        if str(ac.text) == "[分卷阅读]":  # 除去目录中无用的url
            continue
        file.append(str(ac.text) + "  " + str(ac.get('href')) + '\n')  # 标题名加入到列表中
        # file_list_url.append(str(ac.get('href')))   #存入下载地址
        file_list_url.append(ac.attrs['href'])  # 存入下载地址
        file_list_name.append(str(ac.text))  # 存入小说名
        global file_num  # 全局变量必须在函数内部说明 使用 global
        file_num = file_num + 1  # 下载数目
    print("获得目录数量：" + str(file_num))
    write_text("目录.txt", file)  # 写入文件


def write_text(name, text):
    file = open(str(name), 'w')  # 打开文件，覆盖写文件
    if str(type(text)) == r"<class 'list'>":  # 当为列表的时候，逐行输出
        for i in text:
            file.write(i)
    else:
        file.write(str(text))  # 写入文件
    file.flush()  # 刷新缓冲区
    file.close()  # 关闭文件


url = "http://book.zongheng.com/showchapter/963908.html"  # 需要填写的目录列表
if __name__ == '__main__':
    print("------小说下载开始------")
    get_list(url)  # 下载目录
    download()  # 下载章节
    print("\n------小说下载完成------")
