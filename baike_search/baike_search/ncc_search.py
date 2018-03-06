# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import re
import sys,os
import time
#sys.path.append("../")

from whoosh.index import create_in,open_dir

from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from ntcc_woosh import ntcc_woosh

import pymongo
conn = pymongo.MongoClient('43.241.214.180',8080)
db=conn.ncc_search
#search_word='liu huanyong '
#search_type='all'



def ncc_index(request):
    return render(request,"ncc_index.html")

def ncc_show(request):
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    request_page = int(request.GET.get('page', '1'))
    check_box_list=[]
    search_word=''
    region_type=''
    try:
        search_word = request.POST['q']
        check_box_list = request.POST.getlist("check_box_list")
        for region in check_box_list:
            region_type=region
        db.ncc_search.insert({"search_word": search_word, "region_type": region_type})
    except:
        item_list=[]
        for item in db.ncc_search.find():
            item_list.append(item)
        result=item_list[0]
        search_word=result['search_word']
        region_type=result['region_type']
    result_dict={}
    region_list=[]
    value_list=[]
    record_num=0
    result_dict[region_type],record_num=ntcc_woosh.woosh_search(search_word,region_type)
    for region_type,region_result in result_dict.items():
        for item in region_result:
           # print item
            value_list.append(re_h.sub('',item))
    #对结果进行分页处理
    page_list, page_content= page_cut(request_page,value_list)
  #  for region_type,region_result in result_dict.items():
   #     region_list.append(region_type)
    #    value_list.append(region_result)
    #print value_list
    return render(request, "ncc_show.html",
                  {'search_word':search_word,'check_box_list': ' '.join(check_box_list),
                  'region_list':region_list,'value_list':value_list,
                   'record_num':record_num,'page_list':page_list,'page_content':page_content})

def page_cut(request_page,result_list):
    result= Paginator(result_list,100)
    page_nums=result.num_pages
    #获取页面列表
    page_list=[]
    page_content=[]
    for i in range(1,page_nums+1):
        page_list.append(i)
    #显示用户点击页面
    result_page=result.page(request_page)
    #显示用户点击页面内容
    page_content=result_page.object_list
    #对新闻进行正文和来源的分离
    content_list=[]
    for item in page_content:
        title=[]
        item=item.split('\t')
        title.append(item[0])
        title.append(item[1])
        content_list.append(title)
    page_content=content_list
    return page_list,page_content
