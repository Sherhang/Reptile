# -*- coding: utf-8 -*-
"""
爬取文章写入文本
"""

import requests
from bs4 import BeautifulSoup


#  url = 'http://www.en8848.com.cn/article/love/dating/index.html'
# 返回url 的 HTML格式文本
def getHtmlText(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # 自动推断类型
        # print('r.text = ', r.text)
        return r.text
    except:
        return "爬取失败"


# 解析HTML
# 输入参数 html 如 url = 'http://www.en8848.com.cn/article/love/dating/index.html'
# 输出参数 namelist urllist
def getUrlList(namelist, urllist, html='http://www.en8848.com.cn/article/love/dating/index.html'):
    url = 'http://www.en8848.com.cn/'  # 最上层的地址
    # print('html = ', html)
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find(attrs={'class': 'ch_content'})  # find只找到一个满足条件的; 打开网页，查看源码
    # print('t= ', t)
    i = t.find_all('a')
    # print("i = ", i)
    print("len(i) = ", len(i))
    for link in i[1:len(i):2]:  # 这里从下标1开始，步长2, 因为i 的形式是 url，name, url, name ...
        urllist.append(url + link.get('href'))  # 文章链接
        namelist.append(link.get('title'))  # 文章标题列表


def getActicle(html):
    text = []
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find(attrs={'class': 'jxa_content', 'id': 'articlebody'})  # 根据class等字段得到文本
    if t is not None:  # 防止t为None
        # 每一个段落，加到文本里面
        for i in t.findAll('p'):
            text.append(i.text)
        # print(text)
    return "\n".join(text)


def writeToTxt(content):
    with open("getStoryToTxt.txt", 'w') as f:
        f.write(content)


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                      'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    }
    urllist = []
    namelist = []
    for i in range(1, 22):  # 22在网页上查看，一共有21页, [1,22)
        if i == 1:
            url = 'http://www.en8848.com.cn/article/love/dating/index.html'
        else:
            url = 'http://www.en8848.com.cn/article/love/dating/index_' + str(i) + '.html'
        print("正在爬取第%s页的英语短文链接：" % (i))
        print(url + '\n')
        html = getHtmlText(url, headers)
        getUrlList(namelist, urllist, html)
        print('len(namelist) = ', len(namelist))
        print('len(urllist) = ', len(urllist))
    print("爬取链接完成")

    # 写入文件
    f = open("C:/Users/EE526/Desktop/EnglishStoryInTxt.txt", 'w', encoding='utf-8')  # 覆盖写入
    for i in range(len(urllist)):
        html = getHtmlText(urllist[i], headers)  # 对每一个子链接解析
        title = namelist[i]
        if title is None:
            title = 'unknown'
        print('Article ' + str(i + 1))
        content = '\n\nArticle' + str(i + 1) + ':  ' + title + '\n' + getActicle(html)  #
        # print(content)
        f.write(content)
    f.close()
    print("写入完成！")


if __name__ == '__main__':
    main()
