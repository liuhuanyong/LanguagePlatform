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
from book_search_index import book_index
import pymongo
conn = pymongo.MongoClient('101.200.148.213',1026)
db=conn.douban_books

def book_search_index(request):
    return render(request,'book_search_index.html')

def book_search_home(request):
    record_num=0
    book_all_list=[]
    search_word = request.GET['q']
    book_list,record_num=book_index.search_index(search_word)
    try:
        for book_name in book_list:
            book_dict={}
            book_dict['book_name']=book_name
            book_dict['book_basic_info']=db.douban_books.find({'book_name':book_name})[0]['book_basic_info']
            book_dict['book_link']="/book_search_show/?q=%s"%book_name
            book_dict['book_image'] = db.douban_books.find({'book_name': book_name})[0]['book_image']
            book_dict['book_tags'] = db.douban_books.find({'book_name': book_name})[0]['book_tags']
            book_all_list.append(book_dict)
    except:
        pass
    return render(request,'book_search_home.html',{'book_list':book_all_list,'record_num':record_num,'search_word':search_word})

def book_search_show(request):
   search_word = request.GET['q'].encode('utf-8')
   book_id = ''
   book_name =['']
   book_score =['']
   book_basic_info = ['']
   book_comment = ['']
   book_short_comment = ['']
   book_reading_note = ['']
   book_content = ['']
   book_introduction = ['']
   book_tags = ['']
   book_douban_link = ['']
   book_image =['']
   book_author =['']
   book_publish_house = ['']
   book_publish_time = ['']
   book_pages =['']
   book_price =['']
   book_series =['']
   book_kind = ['']
   book_isbn = ['']
   book_sub_name = ['']
   book_translator = ['']
   try:
       item=db.douban_books.find({'book_name':search_word})[0]
       book_id=item['book_id']
       book_name=item['book_name'],
       book_score=item['book_score'],
       book_basic_info=item['book_basic_info'],
       book_comment=item['book_comment'],
       book_short_comment=item['book_short_comment'],
       book_reading_note=item['book_reading_note'],
       book_content=item['book_content'],
       book_introduction=item['book_introduction'],
       book_tags=item['book_tags'],
       book_douban_link=item['book_douban_link'],
       book_image=item['book_image'],
       book_author=item['book_author'],
       book_publish_house=item['book_publish_house'],
       book_publish_time=item['book_publish_time'],
       book_pages=item['book_pages'],
       book_price=item['book_price'],
       book_series=item['book_series'],
       book_kind=item['book_kind'],
       book_isbn=item['book_isbn'],
       book_sub_name=item['book_sub_name'],
       book_translator=item['book_translator'],
   except:
       pass
   #对评论进行分条显示
   book_comment=''.join(book_comment[0])
   count_comment=0
   comment_list=[]
   for item in book_comment.split(';'):
       if item !="":
           count_comment+=1
           comment_sublist=[]
           comment_sublist.append(count_comment)
           comment_sublist.append(item)
           comment_list.append(comment_sublist)
   # 对评论进行分条显示
   book_short_comment = ''.join(book_short_comment[0])
   count_comment = 0
   short_comment_list = []
   for item in book_short_comment.split(';'):
       if item != "":
           count_comment += 1
           comment_sublist = []
           comment_sublist.append(count_comment)
           comment_sublist.append(item)
           short_comment_list.append(comment_sublist)
    # 对评论进行分条显示
   book_reading_note= ''.join(book_reading_note[0])
   count_comment = 0
   reading_note_list = []
   for item in book_reading_note.split(';'):
       if item != "":
           count_comment += 1
           comment_sublist = []
           comment_sublist.append(count_comment)
           comment_sublist.append(item)
           reading_note_list.append(comment_sublist)
   return render(request,'book_search_show.html',{
                            'search_word':search_word,
                            'book_id':book_id,
                            'book_name':book_name[0],
                            'book_score':book_score[0],
                            'book_basic_info':book_basic_info[0],
                            'book_comment':comment_list,
                            'book_short_comment':short_comment_list,
                            'book_reading_note':reading_note_list,
                            'book_content':book_content[0],
                            'book_introduction':book_introduction[0].replace(';','\n'),
                            'book_tags':book_tags[0],
                            'book_douban_link':book_douban_link[0],
                            'book_image':book_image[0],
                            'book_author':book_author[0],
                            'book_publish_house':book_publish_house[0],
                            'book_publish_time':book_publish_time[0],
                            'book_pages':book_pages[0],
                            'book_price':book_price[0],
                            'book_series':book_series[0],
                            'book_kind':book_kind[0],
                            'book_isbn':book_isbn[0],
                            'book_sub_name':book_sub_name[0],
                            'book_translator': book_translator[0],
                            })
