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
from novel_whoosh import search
import pymongo
conn = pymongo.MongoClient('43.241.214.180',8080)
db=conn.novel_books


def novel_search_index(request):
    return render(request,"novel_search_index.html")

def author_search_index(request):
    return render(request,"author_search_index.html")

def author_search_result(request):
    search_word = request.GET['q']
    author_list, author_num = search.author_index(search_word)
    author_data_list=[]
    author_data={}
    for author_name in author_list:
        author_dict = {}
        author_dict['author_name'] = author_name
        author_link = "/author_search_show/?q=" + author_name
        author_dict['author_link'] = author_link
        author_data_list.append(author_dict)
    author_data['author_num'] = author_num
    author_data['author_data_list'] = author_data_list
    author_data['search_word'] = search_word

    return render(request, "author_search_result.html",author_data)

def author_search_show(request):

    search_word = request.GET['q'].encode('utf-8')
    data={}
    length_all=0
    words_all = 0
    words_type = 0
    key_words=''
    words_adj=''
    words_noun=''
    words_verb=''
    author=''
    count=0
    count_word1=0
    count_word2=0
    count_word3=0
    count_word4=0
    count_word5=0
    count_word6=0
    word1_dict = {}
    word2_dict = {}
    word3_dict = {}
    word4_dict = {}
    word5_dict = {}
    word6_dict = {}
    word1_list = []
    word2_list = []
    word3_list = []
    word4_list = []
    word5_list = []
    word6_list = []

    for item in db.author_info.find({"author":search_word}):
        count+=1
        keywords=[]
        noun_list=[]
        adj_list=[]
        verb_list=[]
        author=item['author']
        for word in item['key_words'].split(';'):
            keywords.append(word.split('_')[0])
        key_words=' '.join(keywords[:51])

        for word in item['words_noun'].split(';'):
            word_item=(word.split('_')[0]).split('/')[0]
            noun_list.append(word_item)
        words_noun=' '.join(noun_list[:51])

        for word in item['words_adj'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            adj_list.append(word_item)
        words_adj = ' '.join(adj_list[:51])

        for word in item['words_veb'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            verb_list.append(word_item)
        words_verb = ' '.join(verb_list[:51])

    book_list=[]

    for item in db.book_info.find({'author':search_word}):
        count+=1
        book=[]
        book_name=item['name']
        book_type=item['novel_type']
        book_word_types = item['words_info'][0]
        book_word_all = item['words_info'][1]
        book_link="/novel_book_search_show/?q=" + book_name
        book.append(book_name)
        book.append(book_type)
        book.append(book_word_all)
        book.append(book_word_types)
        book.append(book_link)
        book_list.append(book)
        length=int(item['length'])
        length_all+=length

        word_type = item['words_info'][0]
        words_type += int(word_type)

        word_all = item['words_info'][1]
        words_all += int(word_all)

        word1_count = item['words_info'][2]
        count_word1 += int(word1_count)

        word1_count = item['words_info'][2]
        count_word1+=int(word1_count)
        word2_count = item['words_info'][3]
        count_word2+=int(word2_count)
        word3_count = item['words_info'][4]
        count_word3+=int(word3_count)
        word4_count = item['words_info'][5]
        count_word4 += int(word4_count)
        word5_count = item['words_info'][6]
        count_word5 += int(word5_count)
        word6_count = item['words_info'][7]
        count_word6 += int(word6_count)

        for word in item['words_1'].split(';'):
            try:
                word_word=(word.split('_')[0])
                word_count=int((word.split('_')[1]))
                if word_word not in word1_dict:
                    word1_dict[word_word]=word_count
                else:
                    word1_dict[word_word]+=word_count
            except:
                pass

        for word in item['words_2'].split(';'):
            try:
                word_word=(word.split('_')[0])
                word_count=int((word.split('_')[1]))
                if word_word not in word1_dict:
                    word2_dict[word_word]=word_count
                else:
                    word2_dict[word_word]+=word_count
            except:
                pass

        for word in item['words_3'].split(';'):
            try:
                word_word=(word.split('_')[0])
                word_count=int((word.split('_')[1]))
                if word_word not in word3_dict:
                    word3_dict[word_word]=word_count
                else:
                    word3_dict[word_word]+=word_count
            except:
                pass

        for word in item['words_4'].split(';'):
            try:
                word_word=(word.split('_')[0])
                word_count=int((word.split('_')[1]))
                if word_word not in word4_dict:
                    word4_dict[word_word]=word_count
                else:
                    word4_dict[word_word]+=word_count
            except:
                pass

        for word in item['words_5'].split(';'):
            try:
                word_word=(word.split('_')[0])
                word_count=int((word.split('_')[1]))
                if word_word not in word5_dict:
                    word5_dict[word_word]=word_count
                else:
                    word5_dict[word_word]+=word_count
            except:
                pass

        for word in item['words_6'].split(';'):
            try:
                word_word=(word.split('_')[0])
                word_count=int((word.split('_')[1]))
                if word_word not in word1_dict:
                    word6_dict[word_word]=word_count
                else:
                    word6_dict[word_word]+=word_count
            except:
                pass

    word1_dict=sorted(word1_dict.items(),key=lambda asd:asd[1],reverse=True)
    for item in word1_dict:
        word1_list.append(item[0])
    word1_list=' '.join(word1_list[:51])

    word2_dict = sorted(word2_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word2_dict:
        word2_list.append(item[0])
    word2_list = ' '.join(word2_list[:51])

    word3_dict = sorted(word3_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word3_dict:
        word3_list.append(item[0])
    word3_list = ' '.join(word3_list[:51])

    word4_dict = sorted(word4_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word4_dict:
        word4_list.append(item[0])
    word4_list = ' '.join(word4_list[:51])

    word5_dict = sorted(word5_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word5_dict:
        word5_list.append(item[0])
    word5_list = ' '.join(word5_list[:51])

    word6_dict = sorted(word6_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word6_dict:
        word6_list.append(item[0])
    word6_list = ' '.join(word6_list[:51])


    length_all=int(float(length_all)/float(count))
    words_all = int(float(words_all) / float(count))
    words_type = int(float(words_type) / float(count))
    count_word1 = int(float(count_word1)/float(count))
    count_word2 = int(float(count_word2)/float(count))
    count_word3 = int(float(count_word3)/float(count))
    count_word4 = int(float(count_word4)/float(count))
    count_word5 = int(float(count_word5)/float(count))
    count_word6 = int(float(count_word6)/float(count))

    #count,word
    data['count_word1'] = count_word1
    data['count_word2'] = count_word2
    data['count_word3'] = count_word3
    data['count_word4'] = count_word4
    data['count_word5'] = count_word5
    data['count_word6'] = count_word6
    #words,count
    data['word1_list'] = word1_list
    data['word2_list'] = word2_list
    data['word3_list'] = word3_list
    data['word4_list'] = word4_list
    data['word5_list'] = word5_list
    data['word6_list'] = word6_list


    data['length_all']=length_all
    data['words_all']=words_all
    data['words_type']=words_type
    data['book_info']=book_list
    data['key_words']=key_words
    data['words_noun']=words_noun
    data['words_adj']=words_adj
    data['words_verb']=words_verb
    data['author']=author


    return render(request,'author_search_show.html',data)

def novel_type_search_index(request):
    return render(request,"novel_type_search_index.html")

def novel_type_search_result(request):

    search_word = request.GET['q']
    type_list, type_num = search.type_index(search_word)
    type_data_list = []
    type_data = {}
    for type_name in type_list:
        type_dict = {}
        type_dict['type_name'] = type_name
        type_link = "/novel_type_search_show/?q=" + type_name
        type_dict['type_link'] = type_link
        type_data_list.append(type_dict)
    type_data['type_num'] = type_num
    type_data['type_data_list'] = type_data_list
    type_data['search_word'] = search_word
    return render(request, "novel_type_search_result.html",type_data)

def novel_type_search_show(request):

    search_word = request.GET['q'].encode('utf-8')
    data = {}
    length_all = 0
    words_all = 0
    words_type = 0
    key_words = ''
    words_adj = ''
    words_noun = ''
    words_verb = ''
    author = ''
    count = 0
    count_word1 = 0
    count_word2 = 0
    count_word3 = 0
    count_word4 = 0
    count_word5 = 0
    count_word6 = 0
    word1_dict = {}
    word2_dict = {}
    word3_dict = {}
    word4_dict = {}
    word5_dict = {}
    word6_dict = {}
    word1_list = []
    word2_list = []
    word3_list = []
    word4_list = []
    word5_list = []
    word6_list = []

    for item in db.novel_info.find({"novel_type": search_word}):
        count += 1
        keywords = []
        noun_list = []
        adj_list = []
        verb_list = []
        for word in item['key_words'].split(';'):
            keywords.append(word.split('_')[0])
        key_words = ' '.join(keywords[:51])

        for word in item['words_noun'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            noun_list.append(word_item)
        words_noun = ' '.join(noun_list[:51])

        for word in item['words_adj'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            adj_list.append(word_item)
        words_adj = ' '.join(adj_list[:51])

        for word in item['words_veb'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            verb_list.append(word_item)
        words_verb = ' '.join(verb_list[:51])

    book_list = []

    for item in db.book_info.find({'novel_type': search_word}):
        count += 1
        book = []
        novel_type=item['novel_type']
        book_name = item['name']
        book_author = item['author']
        book_word_types = item['words_info'][0]
        book_word_all = item['words_info'][1]
        book_link = "/novel_book_search_show/?q=" + book_name
        book.append(book_name)
        book.append(book_author)
        book.append(book_word_all)
        book.append(book_word_types)
        book.append(book_link)
        book_list.append(book)
        length = int(item['length'])
        length_all += length

        word_type = item['words_info'][0]
        words_type += int(word_type)

        word_all = item['words_info'][1]
        words_all += int(word_all)

        word1_count = item['words_info'][2]
        count_word1 += int(word1_count)

        word1_count = item['words_info'][2]
        count_word1 += int(word1_count)
        word2_count = item['words_info'][3]
        count_word2 += int(word2_count)
        word3_count = item['words_info'][4]
        count_word3 += int(word3_count)
        word4_count = item['words_info'][5]
        count_word4 += int(word4_count)
        word5_count = item['words_info'][6]
        count_word5 += int(word5_count)
        word6_count = item['words_info'][7]
        count_word6 += int(word6_count)

        for word in item['words_1'].split(';'):
            try:
                word_word = (word.split('_')[0])
                word_count = int((word.split('_')[1]))
                if word_word not in word1_dict:
                    word1_dict[word_word] = word_count
                else:
                    word1_dict[word_word] += word_count
            except:
                pass

        for word in item['words_2'].split(';'):
            try:
                word_word = (word.split('_')[0])
                word_count = int((word.split('_')[1]))
                if word_word not in word1_dict:
                    word2_dict[word_word] = word_count
                else:
                    word2_dict[word_word] += word_count
            except:
                pass

        for word in item['words_3'].split(';'):
            try:
                word_word = (word.split('_')[0])
                word_count = int((word.split('_')[1]))
                if word_word not in word3_dict:
                    word3_dict[word_word] = word_count
                else:
                    word3_dict[word_word] += word_count
            except:
                pass

        for word in item['words_4'].split(';'):
            try:
                word_word = (word.split('_')[0])
                word_count = int((word.split('_')[1]))
                if word_word not in word4_dict:
                    word4_dict[word_word] = word_count
                else:
                    word4_dict[word_word] += word_count
            except:
                pass

        for word in item['words_5'].split(';'):
            try:
                word_word = (word.split('_')[0])
                word_count = int((word.split('_')[1]))
                if word_word not in word5_dict:
                    word5_dict[word_word] = word_count
                else:
                    word5_dict[word_word] += word_count
            except:
                pass

        for word in item['words_6'].split(';'):
            try:
                word_word = (word.split('_')[0])
                word_count = int((word.split('_')[1]))
                if word_word not in word1_dict:
                    word6_dict[word_word] = word_count
                else:
                    word6_dict[word_word] += word_count
            except:
                pass

    word1_dict = sorted(word1_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word1_dict:
        word1_list.append(item[0])
    word1_list = ' '.join(word1_list[:51])

    word2_dict = sorted(word2_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word2_dict:
        word2_list.append(item[0])
    word2_list = ' '.join(word2_list[:51])

    word3_dict = sorted(word3_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word3_dict:
        word3_list.append(item[0])
    word3_list = ' '.join(word3_list[:51])

    word4_dict = sorted(word4_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word4_dict:
        word4_list.append(item[0])
    word4_list = ' '.join(word4_list[:51])

    word5_dict = sorted(word5_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word5_dict:
        word5_list.append(item[0])
    word5_list = ' '.join(word5_list[:51])

    word6_dict = sorted(word6_dict.items(), key=lambda asd: asd[1], reverse=True)
    for item in word6_dict:
        word6_list.append(item[0])
    word6_list = ' '.join(word6_list[:51])

    length_all = int(float(length_all) / float(count))
    words_all = int(float(words_all) / float(count))
    words_type = int(float(words_type) / float(count))
    count_word1 = int(float(count_word1) / float(count))
    count_word2 = int(float(count_word2) / float(count))
    count_word3 = int(float(count_word3) / float(count))
    count_word4 = int(float(count_word4) / float(count))
    count_word5 = int(float(count_word5) / float(count))
    count_word6 = int(float(count_word6) / float(count))

    # count,word
    data['count_word1'] = count_word1
    data['count_word2'] = count_word2
    data['count_word3'] = count_word3
    data['count_word4'] = count_word4
    data['count_word5'] = count_word5
    data['count_word6'] = count_word6
    # words,count
    data['word1_list'] = word1_list
    data['word2_list'] = word2_list
    data['word3_list'] = word3_list
    data['word4_list'] = word4_list
    data['word5_list'] = word5_list
    data['word6_list'] = word6_list

    data['length_all'] = length_all
    data['words_all'] = words_all
    data['words_type'] = words_type
    data['book_info'] = book_list
    data['key_words'] = key_words
    data['words_noun'] = words_noun
    data['words_adj'] = words_adj
    data['words_verb'] = words_verb
    data['author'] = author
    data['novel_type']=novel_type
    return render(request,"novel_type_search_show.html",data)

def novel_book_search_index(request):
    return render(request,"novel_book_search_index.html")

def novel_book_search_result(request):
    search_word = request.GET['q']
    book_list, book_num = search.book_index(search_word)
#    print book_list,book_num
    book_data_list = []
    book_data = {}
    for book_name in book_list:
 #       print book_name
        book_dict = {}
        book_dict['book_name'] = book_name
        book_link = "/novel_book_search_show/?q=" + book_name
        book_dict['book_link'] = book_link
        book_data_list.append(book_dict)
    book_data['book_num'] = book_num
    book_data['book_data_list'] = book_data_list
    book_data['search_word'] = search_word
    return render(request, "novel_book_search_result.html",book_data)


def novel_book_search_show(request):
    search_word_1 = request.GET['q']
    search_word=search_word_1.encode('utf-8')
  #  print search_word
    data = {}
    key_words = ''
    words_adj = ''
    words_noun = ''
    words_verb = ''
    author = ''
    length=''
    name=''
    novel_type=''
    word_types = ''
    word_all = ''
    word1_count = ''
    word2_count = ''
    word3_count = ''
    word4_count = ''
    word5_count = ''
    word6_count = ''
    word1_list = ''
    word2_list = ''
    word3_list = ''
    word4_list = ''
    word5_list = ''
    word6_list = ''
    for item in db.book_info.find({"name": search_word}):
   #     print item
        keywords = []
        noun_list = []
        adj_list = []
        verb_list = []
        for word in item['keywords'].split(';'):
            keywords.append(word.split('_')[0])
        key_words = ' '.join(keywords)

        for word in item['words_noun'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            noun_list.append(word_item)
        words_noun = ' '.join(noun_list[:51])

        for word in item['words_adj'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            adj_list.append(word_item)
        words_adj = ' '.join(adj_list[:51])

        for word in item['words_verb'].split(';'):
            word_item = (word.split('_')[0]).split('/')[0]
            verb_list.append(word_item)
        words_verb = ' '.join(verb_list[:51])
        name = item['name']
        novel_type = item['novel_type']
        length=item['length']
        author = item['author']
        word_types=item['words_info'][0]
        word_all=item['words_info'][1]
        word1_count=item['words_info'][2]
        word2_count = item['words_info'][3]
        word3_count = item['words_info'][4]
        word4_count = item['words_info'][5]
        word5_count = item['words_info'][6]
        word6_count = item['words_info'][7]

        word1_item = []
        for word in item['words_1'].split(';'):
            word_item = (word.split('_')[0])
            word1_item.append(word_item)
        word1_list = ' '.join(word1_item[:51])

        word2_item = []
        for word in item['words_2'].split(';'):
            word_item = (word.split('_')[0])
            word2_item.append(word_item)
        word2_list = ' '.join(word2_item[:51])

        word3_item = []
        for word in item['words_3'].split(';'):
            word_item = (word.split('_')[0])
            word3_item.append(word_item)
        word3_list = ' '.join(word3_item[:51])



        word4_item = []
        for word in item['words_4'].split(';'):
            word_item = (word.split('_')[0])
            word4_item.append(word_item)
        word4_list = ' '.join(word4_item[:51])


        word5_item = []
        for word in item['words_5'].split(';'):
            word_item = (word.split('_')[0])
            word5_item.append(word_item)
        word5_list = ' '.join(word5_item[:51])

        word6_item = []
        for word in item['words_6'].split(';'):
            word_item = (word.split('_')[0])
            word6_item.append(word_item)
        word6_list = ' '.join(word6_item[:51])

    data['book_link']="/book_search_show/?q=" + search_word_1
    data['key_words'] = key_words
    data['words_noun'] = words_noun
    data['words_adj'] = words_adj
    data['words_verb'] = words_verb
    data['author'] = author
    data['name']=name
    data['novel_type']=novel_type
    data['word_types']=word_types
    data['word_all']=word_all

    data['word1_count']=word1_count
    data['word2_count']=word2_count
    data['word3_count']=word3_count
    data['word4_count']=word4_count
    data['word5_count']=word5_count
    data['word6_count']=word6_count

    data['word1_list']=word1_list
    data['word2_list']=word2_list
    data['word3_list']=word3_list
    data['word4_list']=word4_list
    data['word5_list']=word5_list
    data['word6_list']=word6_list
    data['length']=length

    return render(request,"novel_book_search_show.html",data)
