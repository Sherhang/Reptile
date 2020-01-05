#!/home/yehang/anaconda3/envs/Spider/bin/python3
# -*- coding: utf-8 -*-
"""
 beautifulSoup 库基本使用
"""

import requests
from bs4 import BeautifulSoup

url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'  # 网址
status = requests.get(url)  # 得到响应，包含响应状态码，如200
status.encoding = 'gb'  # 原网页是GB格式的编码
html = status.text  # 得到html格式的文本
# print(html)
soup = BeautifulSoup(html, "html.parser")
lists = soup.find_all('dd')
links = []
names = []
for l in lists:
    link = l.find('a')
    links.append('http://www.tom61.com/' + link.get('href'))
    names.append(link.get('title'))
print(links)  # 所有文章的链接
for link in links:
    try:
        status = requests.get(link, timeout=3)  # 响应
        status.encoding = status.apparent_encoding  # 自动推断类型
        html = status.text  # 得到HTML
        soup = BeautifulSoup(html, 'html.parser')  # bs解析HTML
        # print(soup)
        article = soup.find('div', attrs={"class": "t_news"})
        article = article.find('h1').text  # 找标题
        print(article)
        paras = soup.find_all('p')  # 寻找所有段落
        for p in paras:
            print(p.text)  # 得到文章的每一段
    except:
        print("爬取失败")
        break
