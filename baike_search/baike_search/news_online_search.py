# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
import re
import os
# coding=utf-8
#coding='utf-8'
import urllib,urllib2
import os
from urllib import quote
import re
from BeautifulSoup import *
import jieba.posseg as pseg
import jieba.analyse
import time
#开始进行热点事件分析
def online_news_index(request):
    return render(request, 'news_online_index.html')
def online_news_search(request):
    word="英国脱欧"
    try:
        word = request.GET['q'].encode('utf-8')
    except:
        pass
    search_word = quote(word)
    link_list = []
    date_list = []
    title_list = []
    num_result = 0
    page_max = 1
    # 先获取第一页，确定总数
    url = "http://search.sina.com.cn/?country=us&t=keyword&c=news&ie=utf-8&q=" + search_word + "&range=title&page=1"
    html = urllib.urlopen(url).read().decode('gbk').encode('utf-8')
    for num_result in re.findall(r'<div class="l_v2">找到相关新闻(.*)篇</div>', html):
        num_result = num_result.replace(',', '')
        page_max = int(num_result) / 20
    if page_max < 1:
        page_max = 1
    # 只获取前十页文本
    if page_max < 10:
        page_end = page_max
    if page_max > 10:
        page_max = 10
    for page_index in range(1, page_max + 1):
        try:
            url = "http://search.sina.com.cn/?country=us&t=keyword&c=news&ie=utf-8&q=" + search_word + "&range=title&page=%s" % page_index
            print url
            html = get_html(url)
            link, date, title = html_parser(html)
            for item in link:
                link_list.append(item)
            for item in date:
                date_list.append(item)
            for item in title:
                title_list.append(item)
        except:
            pass
    news_dict = title_process(date_list, title_list, link_list)
    title_highwords_dict, title_keywords_dict = title_mining(news_dict)
    #print "***********每日新闻信息***************"
    news_title_list=[]
    news_highwords_list=[]
    news_keywords_list=[]
    for item in sorted(news_dict.iteritems(),key=lambda asd:asd[0],reverse=True):
        date=item[0]
        content=item[1]
        news_title_pair=[]
        news_title_pair.append(date)
        news_title_pair.append(' '.join(content.split(';')[:2]))
        news_title_list.append(news_title_pair)
    #存放高频词
    for item in sorted(title_highwords_dict.iteritems(),key=lambda asd:asd[0],reverse=True):
        date=item[0]
        content=item[1]
        news_highwords_pair = []
        news_highwords_pair.append(date)
        news_highwords_pair.append(' '.join(content.split(';')[:11]))
        news_highwords_list.append(news_highwords_pair)

    #存放关键词
    for item in sorted(title_keywords_dict.iteritems(), key=lambda asd: asd[0], reverse=True):
        date = item[0]
        content = item[1]
        news_keywords_pair = []
        news_keywords_pair.append(date)
        news_keywords_pair.append(' '.join(content.split(';')[:11]))
        news_keywords_list.append(news_keywords_pair)

    return render(request,'news_online_show.html',{'search_word':word,'news_title_list':news_title_list,
                            'news_highwords_list':news_highwords_list,'news_keywords_list':news_keywords_list,
                           })

#通过url，读取html文件
def get_html(url):
    req_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }
    req_timeout = 5
    req = urllib2.Request(url, None, req_header)
    resp = urllib2.urlopen(req, None, req_timeout)
    html = resp.read().decode('gbk').encode('utf-8')
    #html = urllib.urlopen(url).read().decode('gbk').encode('utf-8')
    return html

#对得到的html文件进行解析，得到链接，标题等
def html_parser(html):
    #获取链接
    link_list=[]
    date_list=[]
    title_list=[]
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    #获取链接，并将链接存入到链接列表中
    for link_result in re.findall("""h2><a href="(.*.shtml)" target="_blank">""",html):
       # print link_result
        link_list.append(link_result)
    #从链接中抽取时间，并存入到时间列表中
    for link in link_list:
        date=link.split('/')[-2].replace('-','')
        #print date
        date_list.append(date)
    #获取新闻标题
    for title_result in re.findall("""target="_blank">(.*)</a> <span class="fgray_time">""", html):
        title_result=re_h.sub('', title_result)
        if title_result !='':
        #print title_result
            title_list.append(title_result)

    return link_list,date_list,title_list

#对对标题结果进行处理
def title_process(date_list,title_list,link_list):
    news_dict = {}
    news_list = []
    # 将新闻标题与时间信息相结合，形成新的标题串
    length = 0
    if len(title_list) < len(link_list):
        length = len(title_list)
    if len(title_list) > len(link_list):
        length = len(link_list)
    if len(title_list) == len(link_list):
        length = len(title_list)
        # 获取新闻列表长度，进行整合处理
    for i in range(length):
        news_pair = date_list[i] + ';' + title_list[i]
        news_list.append(news_pair)
    # 将新闻标题依据新闻时间进行打包，形成字典形式
    for news in news_list:
        date = news.split(';')[0]
        title = news.split(';')[1]
        if date not in news_dict:
            news_dict[date] = title + ';'
        else:
            news_dict[date] += title + ';'
    # 对新闻进行去重处理
    for key, value in news_dict.items():
        value = ';'.join(list(set(value.split(';'))))
        news_dict[key] = value

    return news_dict

 #对标题进行文本分析
def title_mining(news_dict):
    title_highwords_dict={}
    title_keywords_dict={}
    for date,date_title in news_dict.items():
        word_list=[]
        word_dict={}
        high_words=[]#高频词列表
        key_words=[]#关键词列表
        for item in pseg.cut(date_title):
            if item.flag not in ['x','w','u','uj','c','p','q','o','r','wp','ws']:
                if len(item.word)>1:
                    word_list.append(item.word)
        for word in word_list:
            if word not in word_dict:
                word_dict[word]=1
            else:
                word_dict[word]+=1
        word_dict=sorted(word_dict.iteritems(), key=lambda d: d[1], reverse=True)
        for item in word_dict:
            high_words.append(item[0])
       # print date+"high_words:"+';'.join(high_words[:11])#输出排在前10位的高频词
        key_words=jieba.analyse.extract_tags(date_title, 10)
       # print date+"key_words:"+";".join(key_words)
        title_highwords_dict[int(date)]=';'.join(high_words[:11])
        title_keywords_dict[int(date)]=';'.join(key_words)
        #分别对高频词表、关键词表进行时间排序

    #title_highwords_dict=dict(sorted(title_highwords_dict.iteritems(), key=lambda d: d[0], reverse=True))
    #title_keywords_dict=dict(sorted(title_keywords_dict.iteritems(), key=lambda d: d[0], reverse=True))

    return title_highwords_dict,title_keywords_dict
