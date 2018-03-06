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
db=conn.person


def person_relation_search_index(request):
    return render(request,'person_relation_search_index.html')

def person_relation_search_show(request):
    rel_list = []
    relation_list = []
    name_story = "红楼梦"
    category_dict = {}
    person_list = []
    category_list = []
    weight_list = [3,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5,3,3,3,3,3,3,3,3]
                 # 暂时限定最多人数为100人
    name_story = request.GET['q'].encode('utf-8')
    category_dict[name_story] = 0
    for result in db.person_relation.find({'name_story':name_story}):
        #进行人物类别存储
        person_2 = result['name_person2']
        person_relation = result['rel_type']
        category_dict[person_2] = int(person_relation) + 1
        #进行关系存储
        relation = []
        relation.append(result['name_person1'])
        relation.append(result['person_relation'])
        relation.append(result['name_person2'])
        if relation not in relation_list:
            relation_list.append(relation)
    rel_list = relation_list
    for person, person_category in category_dict.items():
        person_list.append(person)
        category_list.append(person_category)
    #通过人物，遍历输入人物的信息
    person_show_list=[]
    for person in person_list:
        try:
            person_dict={}
            person_dict['person_name']=person
            person_dict['person_img']=db.person.find({'person_name':person})[0]['person_img']
            person_dict['person_introduction'] = db.person.find({'person_name': person})[0]['person_introduction']
            person_dict['person_infobox']=db.person.find({'person_name': person})[0]['person_infobox']
            person_show_list.append(person_dict)
        except:
            pass
    #给予权重
    weight_list = weight_list[:len(person_list) - 1]
    #返回，传递给前端
    return render(request, 'person_relation_search_show.html', {
        'name_story': name_story,
        'rel_list': rel_list,
        'category_list':json.dumps(category_list),
        'person_info':person_list,
        'person_list': json.dumps(person_list),
        'relation_list': json.dumps(relation_list),
        'weight_list': json.dumps(weight_list),
        'person_show_list':person_show_list
    })

