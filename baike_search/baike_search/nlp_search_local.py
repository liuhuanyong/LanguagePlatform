# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
import re
import os
import jieba.posseg as pseg
import jieba.analyse
from sentiment_analysis import sentiment_analysis
import urllib,urllib2
from urllib import quote
from BeautifulSoup import *
from pypinyin import pinyin,lazy_pinyin
from  text_classifier import text_classifier#文本分类器

def nlp_index_local(request):
    return render(request, 'nlp_local_index.html')

def nlp_process_local(request):
    result = {}
    seg_list = []  # 词列表
    key_words = []  # 关键词列表
    person_list = []  # 人物实体
    location_list = []  # 地点实体
    organization_list = []  # 组织实体
    prop_name_list = []  # 专名实体
    word_dict = {}  # 词频字典
    entity_dict = {}  # 实体字典
    entity_list=[]#实体列表
    item_list=[]
    value_list=[]
    key_list=[]
    weight_list=[]
    content="北京语言大学"
    try:
        content = request.GET['q']
    except:
        pass
    #文本分类
    text_score_dict=text_classifier.classifier(content)
    text_score_list=[]
    score_list=[]
    text_target=' '
    for text,score in text_score_dict.items():
        score_pair=[]
        score_list.append(score)
        score_pair.append(text)
        score_pair.append(score)
        text_score_list.append(score_pair)
    text_target_score=sorted(score_list,reverse=True)[0]
    for text,score in text_score_dict.items():
        if score==text_target_score:
            text_target=text
    #情感分析
    seg_text, key_words, word_dict, entity_dict, text_pinyin= text_process(content)
    score_total=0.0
    target_sentiment=''
    sentiment_type_target=''
    sentiment_target_score=1.0
    sentiment_dict={}
    score_sentiment_list=[]
    sentiments_score_list=[]
    score_total, sentiment_dict = sentiment_analysis.sentiment_score(content)
    if float(score_total)<0.0:
        target_sentiment='负面'
    if float(score_total)==0.0:
        target_sentiment='中性'
    if float(score_total)>0.0:
        target_sentiment='正面'
    #获取最有可能的情绪小类
    for item in sorted(sentiment_dict.iteritems(),key=lambda asd:asd[1],reverse=True):
        sentiment_type=item[0]
        score=item[1]
        score_pair = []
        score_sentiment_list.append(float(score))
        score_pair.append(sentiment_type)
        score_pair.append(float(score))
        sentiments_score_list.append(score_pair)
    sentiment_target_score = sorted(score_sentiment_list, reverse=True)[0]
    for sentiment_type, score in sentiment_dict.items():
        if score == sentiment_target_score:
            sentiment_type_target = sentiment_type
    #实体信息统计
    for word_pair in word_dict:
        item_list.append(word_pair[0])
        value_list.append(word_pair[1])
    for key_word in key_words:
        key_list.append(key_word[0])
        weight_list.append(str(float(key_word[1])*150))
    person_list.append('人名')
    person_list.append(entity_dict['person'])
    location_list.append('地名')
    location_list.append(entity_dict['location'])
    organization_list.append('组织机构名')
    organization_list.append(entity_dict['organization'])
    prop_name_list.append('专名')
    prop_name_list.append(entity_dict['prop_name'])
    entity_list.append(person_list)
    entity_list.append(location_list)
    entity_list.append(organization_list)
    entity_list.append(prop_name_list)
    return render(request,'nlp_local_show.html',{'content':content,'item_list': json.dumps(item_list),
                           'value_list': json.dumps(value_list),'word_dict': json.dumps(word_dict),
                           'seg_text':seg_text,'key_words': json.dumps(key_words),
                           'entity_list':entity_list,'key_list': json.dumps(key_list),
                           'weight_list': json.dumps(weight_list),
                           'text_pinyin': text_pinyin,'text_target':text_target,
                           'text_target_score':text_target_score,'text_score_list':text_score_list,
                           'score_total':score_total,'target_sentiment':target_sentiment,
                           'sentiment_type_target':sentiment_type_target,'sentiment_target_score':sentiment_target_score,
                           'sentiments_score_list':sentiments_score_list,
                           })

    #return render(request, 'nlp_net_show.html',result)

#处理文本
#利用jieba,snownlp进行处理
def text_process(content):
    seg_list=[]#词列表
    word_list=[]#词表
    key_words=[]#关键词列表
    person_list=[]#人物实体
    location_list=[]#地点实体
    organization_list=[]#组织实体
    prop_name_list=[]#专名实体
    word_dict={}#词频字典
    entity_dict={}#实体字典
    text_sentiment=0.5
    text_pinyin=''
    text_abstract=''
    for word in pseg.cut(content):
        if word.flag not in ['x','w','ws','wp','o','p','q','u','uj','ul','eng','r','d','m','t','c']:
            word_list.append(word.word)
        if word.flag=='nr':
            person_list.append(word.word)
        if word.flag=='ns':
            location_list.append(word.word)
        if word.flag=='nt':
            organization_list.append(word.word)
        if word.flag=='nz':
            prop_name_list.append(word.word)#获取实体，并分别存入相应实体列表
        word_pair=word.word+'/'+word.flag
        seg_list.append(word_pair)#获取词列表
    person_list='  '.join(set(person_list))
    location_list = '  '.join(set(location_list))
    organization_list = '  '.join(set(organization_list))
    prop_name_list = '  '.join(set(prop_name_list))
    for word in word_list:
        if len(word)>1:
            if word not in word_dict:
                word_dict[word]=1
            else:
                word_dict[word]+=1
    word_dict=sorted(word_dict.iteritems(), key=lambda d:d[1], reverse = True )[:20]
    entity_dict['person']=person_list
    entity_dict['organization']=organization_list
    entity_dict['location']=location_list
    entity_dict['prop_name']=prop_name_list#将实体列表存入实体字典中
    seg_text=' '.join(seg_list)
    key_words=jieba.analyse.textrank(content, topK=10, withWeight=True)#获取关键词
    #获取文本情感倾向，调用snownlp
    try:
        text_pinyin=' '.join(lazy_pinyin(content))
    except:
        pass
   # print unicode(seg_text).encode('utf-8'),key_words,word_dict,entity_dict,unicode(text_pinyin).encode('utf-8'),text_sentiment,text_abstract.encode('utf-8')
    return seg_text,key_words,word_dict,entity_dict,text_pinyin
