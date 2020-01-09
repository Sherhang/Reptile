#!/home/yehang/anaconda3/envs/Spider/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 21:25:45 2019
@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import datetime
import time


def getDays():
    in_date = datetime.datetime(2020, 1, 3)
    today_date = datetime.datetime.today()
    in_days = (today_date - in_date).days
    return str(in_days)


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
def getUrlList(namelist, urllist, html='http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'):
    url = 'http://www.tom61.com/'  # 最上层的地址
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('dl', attrs={'class': 'txt_box'})  # find只找到一个满足条件的; 打开网页，查看源码
    # print('t= ', t)
    i = t.find_all('a')
    # print("i = ", i)
    # print("len(i) = ", len(i))
    for link in i:  # 这里从下标1开始，步长2, 因为i 的形式是 url，name, url, name ...
        urllist.append(url + link.get('href'))  # 文章链接
        namelist.append(link.get('title'))  # 文章标题列表


def getActicle(html):
    text = []
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('div', class_='t_news_txt')  # 根据class等字段得到文本
    if t is not None:  # 防止t为None
        # 每一个段落，加到文本里面
        for i in t.findAll('p'):
            text.append(i.text)
        # print(text)
    return "\n".join(text)


def sendemail(text):
    date_today = time.strftime("%Y-%m-%d", time.localtime())
    msg_from = '2940563940@qq.com'  # 发送方邮箱
    passwd = 'dozeppgiapehdeaj'  # 填入发送方邮箱的授权码
    receivers = ['17552759310@sina.cn']  # 收件人邮箱

    subject = "今日睡前小故事 " + str(date_today)  # 主题

    content = getDays() + ' Days !\n\n⭐⭐⭐⭐⭐❤❤💗❤❤⭐⭐⭐⭐⭐\n\n' + text  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ','.join(receivers)
    ret = 0
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
        s.quit()
        print("发送成功")
        ret = 0
    except smtplib.SMTPException as e:
        print("发送失败: ")
        print(e)
        ret = 1
    return ret


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                      'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    }
    urllist = []
    namelist = []
    for i in range(1, 30):  # 11在网页上查看，一共有11页, [1,22)
        if i == 1:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'
        else:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index_' + str(i) + '.html'
        print("正在爬取第%s页链接：" % (i))
        print(url + '\n')
        html = getHtmlText(url, headers)
        # print(html)
        getUrlList(namelist, urllist, html)
        # print('len(namelist) = ', len(namelist))
        # print('len(urllist) = ', len(urllist))
    print("爬取链接完成")

    # 发送邮件
    day_time = int(time.mktime(datetime.date.today().timetuple()))  # 0点的时间戳
    # print(time.time()-day_time)
    left_time = 23 * 60 * 60  + 0*60 - (time.time() - day_time)  # 第一个参数设置发送时间
    # print(left_time)
    time.sleep(left_time)
    i = 2
    while 1:
        html = getHtmlText(urllist[i], headers)  # 对每一个子链接解析
        title = namelist[i]
        # if title is None:
        #     title = '无题'
        print('\nArticle ' + str(i + 1))
        text = '    ' + title + '\n\n' + getActicle(html)  #
        if len(text) < 20 or title is None:
            i = i + 1
            continue  # 跳过
        print(text)
        delay = 0  # 延迟时间
        while(sendemail(text)):
            delay = delay + 2
            time.sleep(2)
        i = i + 1
        time.sleep(24 * 60 * 60 - delay)  # 间隔时间
        #if i > 100:
        #  break

if __name__ == '__main__':
    main()
