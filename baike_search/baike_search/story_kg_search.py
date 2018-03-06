# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys,os
from operator import itemgetter
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
import re
import os
import pymongo
conn = pymongo.MongoClient('43.241.214.180',8080)
db=conn.story_kg
def story_kg_create_index(request):
    return render(request,'story_kg_create_index.html')
def story_kg_create_show(request):
    person_list=[]
    rel_list=[]
    relation_list=[]
    name_story="default"
    name_person1=''
    person_relation=''
    name_person2=''
    weight_list=[2,10,16,20,27,34,56,78,89,12,
                 16,18,45,4,24,6,12,34,2,5,13,
                 25,8,1,3,5,21,19,28,13,2,4,5,
                 1,6,8,1,2,4,6,12,19,21,31,23,
                 23,45,56,2,4,5,5,7,33,14,6,7,
                 2, 10, 16, 20, 27, 34, 56, 78, 89, 12,
                 16, 18, 45, 4, 24, 6, 12, 34, 2, 5, 13,
                 25, 8, 1, 3, 5, 21, 19, 28, 13, 2, 4, 5,
                 1, 6, 8, 1, 2, 4, 6, 12, 19, 21, 31, 23,
                 23, 45, 56, 2, 4, 5, 5, 7, 33, 14, 6, 7
                 ]#暂时限定最多人数为100人
    try:
        name_story= request.GET['name_story'].encode('utf-8')
        name_person1 = request.GET['name_person1'].encode('utf-8')
        person_relation= request.GET['person_relation'].encode('utf-8')
        name_person2= request.GET['name_person2'].encode('utf-8')
    except:
        pass
    if name_story==''or name_person1=='' or person_relation=='' or name_person2=='':
        name_story="红楼梦"
        name_person1="贾宝玉"
        person_relation="恋人"
        name_person2="林黛玉"
    #将用户创建的记录写入到日志文件当中
    #用户每创建一部小说，则以该小说为名，生成文件，在写入之前，需要判断是否为同一部小说
    db.story_kg.insert({'name_story':name_story,'name_person1':name_person1,
                        'person_relation':person_relation,'name_person2':name_person2})
    #打开生成的小说人物关系文件，进行存储
    for result in db.story_kg.find({'name_story':name_story}):
        relation=[]
        person_list.append(result['name_person1'])
        person_list.append(result['name_person2'])
        #存入人物关系列表
        relation.append(result['name_person1'])
        relation.append(result['person_relation'])
        relation.append(result['name_person2'])
        if relation not in relation_list:
            relation_list.append(relation)
    rel_list=relation_list
    person_list=list(set(person_list))
    weight_list=weight_list[:len(person_list)-1]
    #存储三元组，依次为人物1、人物关系、人物2
    return render(request,'story_kg_create_show.html',{
                                                'name_story':name_story,
                                                'rel_list':rel_list,
                                                'person_list': json.dumps(person_list),
                                                'relation_list': json.dumps(relation_list),
                                                'weight_list': json.dumps(weight_list),
                                                })

def story_kg_search_index(request):
    return render(request,'story_kg_search_index.html')

def story_kg_search_show(request):
    person_list = []
    rel_list = []
    relation_list = []
    name_story = "红楼梦"
    weight_list = [2, 10, 16, 20, 27, 34, 56, 78, 89, 12,
                   16, 18, 45, 4, 24, 6, 12, 34, 2, 5, 13,
                   25, 8, 1, 3, 5, 21, 19, 28, 13, 2, 4, 5,
                   1, 6, 8, 1, 2, 4, 6, 12, 19, 21, 31, 23,
                   23, 45, 56, 2, 4, 5, 5, 7, 33, 14, 6, 7,
                   2, 10, 16, 20, 27, 34, 56, 78, 89, 12,
                   16, 18, 45, 4, 24, 6, 12, 34, 2, 5, 13,
                   25, 8, 1, 3, 5, 21, 19, 28, 13, 2, 4, 5,
                   1, 6, 8, 1, 2, 4, 6, 12, 19, 21, 31, 23,
                   23, 45, 56, 2, 4, 5, 5, 7, 33, 14, 6, 7
                   ]  # 暂时限定最多人数为100人
    name_story = request.GET['q'].encode('utf-8')

    for result in db.story_kg.find({'name_story':name_story}):
        relation = []
        person_list.append(result['name_person1'])
        person_list.append(result['name_person2'])
        # 存入人物关系列表
        relation.append(result['name_person1'])
        relation.append(result['person_relation'])
        relation.append(result['name_person2'])
        if relation not in relation_list:
            relation_list.append(relation)
    rel_list = relation_list
    person_list = list(set(person_list))
    weight_list = weight_list[:len(person_list) - 1]
    return render(request, 'story_kg_search_show.html', {
        'name_story': name_story,
        'rel_list': rel_list,
        'person_list': json.dumps(person_list),
        'relation_list': json.dumps(relation_list),
        'weight_list': json.dumps(weight_list),
    })

