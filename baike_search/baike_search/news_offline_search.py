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
import time
from django.http import HttpResponse
from django.shortcuts import render
import json
import pymongo
conn = pymongo.MongoClient('43.241.214.180',8080)
db = conn.history_keywords_content
#开始进行热点事件分析
def offline_news_index(request):
    return render(request, 'news_offline_index.html')
def offline_news_search(request):
    search_date=request.GET['search_date']
    date=''.join(search_date.split('-')[1:])
    abroad_keywords=[]
    inbroad_keywords = []
    tech_keywords = []
    ent_keywords = []
    edu_keywords = []
    sports_keywords = []
    house_keywords = []
    society_keywords = []
    games_keywords = []
    finance_keywords = []
    auto_keywords = []
    #abroad
    for item in db.history_keywords_content.find({'date':date,'region_type':'abroad'}):
        pair=[]
        pair.append(item['year']+item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        abroad_keywords.append(pair)
    #society
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'society'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        society_keywords.append(pair)

    #auto
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'auto'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        auto_keywords.append(pair)

    #finance
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'finance'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        finance_keywords.append(pair)

    #games
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'games'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        games_keywords.append(pair)

    #sports
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'sports'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        sports_keywords.append(pair)

   # edu
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'edu'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        edu_keywords.append(pair)

    #ent
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'ent'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        ent_keywords.append(pair)

    #inbroad
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'inbroad'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        inbroad_keywords.append(pair)

    #house
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'house'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        house_keywords.append(pair)

    #tech
    for item in db.history_keywords_content.find({'date': date, 'region_type': 'tech'}):
        pair = []
        pair.append(item['year'] + item['date'])
        pair.append(' '.join(item['keywords'].split(';')[:20]))
        tech_keywords.append(pair)

    return render(request,'news_offline_show.html',{'search_date':search_date,'abroad_keywords':abroad_keywords,
                                                    'inbroad_keywords': inbroad_keywords,'ent_keywords':ent_keywords,
                                                    'edu_keywords': edu_keywords,
                                                    'house_keywords': house_keywords,'finance_keywords':finance_keywords,
                                                    'sports_keywords': sports_keywords,
                                                    'auto_keywords': auto_keywords,
                                                    'games_keywords': games_keywords,
                                                    'tech_keywords': tech_keywords,
                                                    'society_keywords': society_keywords,})

