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
db=conn.tecent_words

def word_search_index(request):
    return render(request,'word_semantic_index.html')


def word_search_show(request):
    search_word = request.GET['q'].encode('utf-8')
    data={}
    data['search_word']=search_word
    word_list_auto = []
    word_list_edu = []
    word_list_ent = []
    word_list_finance = []
    word_list_games = []
    word_list_house = []
    word_list_society = []
    word_list_sports = []
    word_list_tech = []

    for item in db.words.find({"word":search_word,"region":'auto'}):
        for word in item['similar_words']:
            word_list_auto.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'edu'}):
        for word in item['similar_words']:
            word_list_edu.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'ent'}):
        for word in item['similar_words']:
            word_list_ent.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'finance'}):
        for word in item['similar_words']:
            word_list_finance.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'games'}):
        for word in item['similar_words']:
            word_list_games.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'house'}):
        for word in item['similar_words']:
            word_list_house.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'society'}):
        for word in item['similar_words']:
            word_list_society.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'sports'}):
        for word in item['similar_words']:
            word_list_sports.append(word[0])

    for item in db.words.find({"word": search_word, "region": 'tech'}):
        for word in item['similar_words']:
            word_list_tech.append(word[0])

    data['auto'] = ' '.join(word_list_auto)
    data['edu'] = ' '.join(word_list_edu)
    data['ent'] = ' '.join(word_list_auto)
    data['finance'] = ' '.join(word_list_finance)
    data['games'] = ' '.join(word_list_games)
    data['house'] = ' '.join(word_list_house)
    data['society'] = ' '.join(word_list_society)
    data['sports'] = ' '.join(word_list_sports)
    data['tech'] = ' '.join(word_list_tech)

    return render(request,'word_semantic_show.html',data)


