# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
import re
import os
import urllib,urllib2
from urllib import quote
from BeautifulSoup import *

#定义网站主页
def index(request):
    return render(request,'index.html')
#定义百科搜索主页
def search_index(request):
    return render(request, 'baike_search_index.html')
#定义个人主页
def about_me(request):
    return render(request, 'about_me.html')
#定义网站介绍页
def about_web(request):
    return render(request, 'about_web.html')
#代码执行区域
def search_show(request):
    result={}
    search_word="北京语言大学"
    try:
        search_word=request.GET['q'].encode('utf-8')
        result['search_word'] = search_word
    except:
        pass
    search_word = quote(search_word)
    url_hudong = "http://www.baike.com/wiki/%s" % search_word
    url_baidu = "http://baike.baidu.com/item/%s" % search_word
    result_hudong,summary=get_attribute_hudong(get_html(url_hudong))
    result_baidu = get_attribute_baidu(get_html(url_baidu))
    result['result_hudong']= result_hudong
    result['result_baidu'] = result_baidu
    result['summary']=summary
    return render(request, 'baike_search_show.html', result)

def get_html(url):
    html = urllib.urlopen(url).read()
    return html

def get_attribute_hudong(html):
    re_h = re.compile('</?\w+[^>]*>')
    soup = BeautifulSoup(html)
    attribute_list=[]
    value_list=[]
    result_list=[]
        # 获得摘要
    summary_result = soup.find(attrs={'class': 'summary'})
    summary = re_h.sub('', str(summary_result)).replace("编辑摘要", '')
    print summary
        # 获得info-box
    for div in soup.findAll(attrs={'class': 'module zoom'}):
        for table_result in div.findAll('table'):
            for tr_result in table_result.findAll('tr'):
                for td in tr_result.findAll('td'):
                    if td.strong is not None and td.span is not None:
                        attribute = re_h.sub('', str(td.strong)).replace('\n', '').replace(' ', '').replace("：",'')
                        value = re_h.sub('', str(td.span)).replace('\n', '').replace(' ', '')
                        attribute_list.append(attribute)
                        value_list.append(value)
    for index in range(len(value_list)):
        pair = []
        pair.append(attribute_list[index])
        pair.append(value_list[index])
        result_list.append(pair)
    return result_list,summary
        # f.write(attribute+value+'\n')

def get_attribute_baidu(html):
    re_h = re.compile('</?\w+[^>]*>')
    soup = BeautifulSoup(html)
        # 获得摘要
    summary_result = soup.find(attrs={'class': 'lemma-summary'})
    summary = re_h.sub('', str(summary_result)).replace("&nbsp;", '').replace('\n', '').replace(' ', '')
        # print summary
        # 获得info-box
    attribute_list = []
    value_list = []
    result_list=[]
    for attribute_result in soup.findAll(attrs={'class': 'basicInfo-item name'}):
        attribute = str(attribute_result).replace("&nbsp;", '')
        attribute = re_h.sub('', attribute)
        attribute_list.append(attribute)
    for value_result in soup.findAll(attrs={'class': 'basicInfo-item value'}):
        value = str(value_result).replace("&nbsp;", '')
        value = re_h.sub('', value).replace('\n', '').replace(' ', '')
        value_list.append(value)
    for index in range(len(value_list)):
        pair=[]
        pair.append(attribute_list[index])
        pair.append(value_list[index])
        result_list.append(pair)
    return result_list









