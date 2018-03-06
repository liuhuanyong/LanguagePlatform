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
from django.core.paginator import Paginator
from job_index import job_index
import pymongo
conn = pymongo.MongoClient('43.241.214.180',8080)
db=conn.lagou_jobs


def job_search_index(request):
    return render(request, "job_search_index.html")


def job_search_show(request):
    search_word = request.GET['q']
    job_list, job_num = job_index.search_index(search_word)
    job_data = {}
    job_data_list=[]
    for job_name in job_list:
        job_dict={}
        job_dict['job_name']=job_name
        job_link="/job_search_result/?q="+job_name
        job_dict['job_link']=job_link
        job_data_list.append(job_dict)
    job_data['job_num'] = job_num
    job_data['job_data_list']=job_data_list
    job_data['search_word']=search_word
    return render(request, "job_search_home.html", job_data)

def job_search_result(request):
    search_word = request.GET['q'].encode('utf-8')
    job_data={}
    for item in db.jobs.find({"job_name":search_word}):
        #advantage

        advantage_list = []
        advantage_list_all = []
        for advantage_pair in item['job_advantage']:
            if len(advantage_pair[0]) > 2:
                pair = advantage_pair[0] + '(' + advantage_pair[1] + ')'
                advantage_list.append(pair)
        advantage_list_all.append(advantage_list[0:4])
        advantage_list_all.append(advantage_list[5:9])
        advantage_list_all.append(advantage_list[10:14])
        advantage_list_all.append(advantage_list[15:19])
        advantage_list_all.append(advantage_list[20:24])
        advantage_list_all.append(advantage_list[25:29])
        advantage_list_all.append(advantage_list[30:34])
        advantage_list_all.append(advantage_list[35:39])
        advantage_list_all.append(advantage_list[40:44])
        advantage_list_all.append(advantage_list[45:49])
        job_data['job_advantage'] = advantage_list_all

        #boss

        boss_list = []
        boss_list_all = []
        for boss_pair in item['job_boss']:
            if len(boss_pair[0]) > 1:
                pair = boss_pair[0] + '(' + boss_pair[1] + ')'
                boss_list.append(pair)
        boss_list_all.append(boss_list[0:4])
        boss_list_all.append(boss_list[5:9])
        boss_list_all.append(boss_list[10:14])
        boss_list_all.append(boss_list[15:19])
        boss_list_all.append(boss_list[20:24])
        boss_list_all.append(boss_list[25:29])
        boss_list_all.append(boss_list[30:34])
        boss_list_all.append(boss_list[35:39])
        boss_list_all.append(boss_list[40:44])
        boss_list_all.append(boss_list[45:49])
        job_data['job_boss'] = boss_list_all

        #full_name

        full_name_list = []
        full_name_list_all = []
        for full_name_pair in item['job_full_name']:
            if len(full_name_pair[0]) > 1:
                pair = full_name_pair[0] + '(' + full_name_pair[1] + ')'
                full_name_list.append(pair)
        full_name_list_all.append(full_name_list[0:4])
        full_name_list_all.append(full_name_list[5:9])
        full_name_list_all.append(full_name_list[10:14])
        full_name_list_all.append(full_name_list[15:19])
        full_name_list_all.append(full_name_list[20:24])
        full_name_list_all.append(full_name_list[25:29])
        full_name_list_all.append(full_name_list[30:34])
        full_name_list_all.append(full_name_list[35:39])
        full_name_list_all.append(full_name_list[40:44])
        full_name_list_all.append(full_name_list[45:49])
        job_data['job_full_name'] = full_name_list_all

        #request
        request_list=[]
        request_list_all=[]
        for request_pair in item['job_request']:
            if len(request_pair[0])>3:
                pair=request_pair[0]+'('+request_pair[1]+')'
                request_list.append(pair)
        request_list_all.append(request_list[0:4])
        request_list_all.append(request_list[5:9])
        request_list_all.append(request_list[10:14])
        request_list_all.append(request_list[15:19])
        request_list_all.append(request_list[20:24])
        request_list_all.append(request_list[25:29])
        request_list_all.append(request_list[30:34])
        request_list_all.append(request_list[35:39])
        request_list_all.append(request_list[40:44])
        request_list_all.append(request_list[45:49])
        job_data['job_request']=request_list_all
        #money

        money_list = []
        money_list_all = []
        for money_pair in item['job_money']:
            if len(money_pair[0]) > 0:
                pair = money_pair[0] + '(' + money_pair[1] + ')'
                money_list.append(pair)
        money_list_all.append(money_list[0:4])
        money_list_all.append(money_list[5:9])
        money_list_all.append(money_list[10:14])
        money_list_all.append(money_list[15:19])
        money_list_all.append(money_list[20:24])
        money_list_all.append(money_list[25:29])
        money_list_all.append(money_list[30:34])
        money_list_all.append(money_list[35:39])
        money_list_all.append(money_list[40:44])
        money_list_all.append(money_list[45:49])
        job_data['job_money'] = money_list_all
        #place

        place_list = []
        place_list_all = []
        for place_pair in item['job_place']:
            if len(place_pair[0]) > 0:
                pair = place_pair[0] + '(' + place_pair[1] + ')'
                place_list.append(pair)
        place_list_all.append(place_list[0:4])
        place_list_all.append(place_list[5:9])
        place_list_all.append(place_list[10:14])
        place_list_all.append(place_list[15:19])
        place_list_all.append(place_list[20:24])
        place_list_all.append(place_list[25:29])
        place_list_all.append(place_list[30:34])
        place_list_all.append(place_list[35:39])
        place_list_all.append(place_list[40:44])
        place_list_all.append(place_list[45:49])
        job_data['job_place'] = place_list_all
        #work
        work_list = []
        work_list_all = []
        for work_pair in item['job_work']:
            if len(work_pair[0]) > 3:
                pair = work_pair[0] + '(' + work_pair[1] + ')'
                work_list.append(pair)
        work_list_all.append(work_list[0:4])
        work_list_all.append(work_list[5:9])
        work_list_all.append(work_list[10:14])
        work_list_all.append(work_list[15:19])
        work_list_all.append(work_list[20:24])
        work_list_all.append(work_list[25:29])
        work_list_all.append(work_list[30:34])
        work_list_all.append(work_list[35:39])
        work_list_all.append(work_list[40:44])
        work_list_all.append(work_list[45:49])
        job_data['job_work'] = work_list_all

        job_data['job_worktime'] = item['job_worktime']
        job_data['job_experience'] = item['job_experience']
        job_data['job_year'] = item['job_year']
        job_data['job_degree'] = item['job_degree']
        job_data['search_word']=search_word
    return render(request,"job_search_show.html",job_data)

