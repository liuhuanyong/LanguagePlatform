"""baike_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from baike_search import search_index,search_show,index,about_me,about_web
from nlp_search_net import nlp_process,nlp_index
from nlp_search_local import nlp_index_local,nlp_process_local
from news_online_search import online_news_index,online_news_search
from ncc_search import ncc_index,ncc_show
from news_offline_search import offline_news_index,offline_news_search
from story_kg_search import story_kg_create_index,story_kg_create_show,\
    story_kg_search_index,story_kg_search_show
from person_relation_search import person_relation_search_index,person_relation_search_show
from book_search import book_search_index,book_search_show,book_search_home
from job_search import job_search_index,job_search_show,job_search_result
from word_semantic_search import word_search_index,word_search_show
from novel_search import novel_book_search_index,novel_search_index,novel_book_search_show,\
    novel_type_search_index,novel_type_search_show,author_search_index,author_search_show,\
    novel_book_search_result,novel_type_search_result,author_search_result
urlpatterns = [
    url(r'^$', word_search_index),
    url(r'^admin/', admin.site.urls),

    url(r'^search_index/', search_index),
    url(r'^search_show/', search_show),

    url(r'^index/', index),

    url(r'^nlp_index/', nlp_index),
    url(r'^nlp_process/', nlp_process),

    url(r'^about_me/', about_me),

    url(r'^about_web/', about_web),

    url(r'^nlp_index_local/', nlp_index_local),
    url(r'^nlp_process_local/', nlp_process_local),

    url(r'^online_news_index/', online_news_index),
    url(r'^online_news_search/',online_news_search),

    url(r'^ncc_index/',ncc_index),
    url(r'^ncc_show/',ncc_show),

    url(r'^offline_news_index/',offline_news_index),
    url(r'^offline_news_search/',offline_news_search),

    url(r'^story_kg_create_index/',story_kg_create_index),
    url(r'^story_kg_create_show/',story_kg_create_show),
    url(r'^story_kg_search_index/',story_kg_search_index),
    url(r'^story_kg_search_show/',story_kg_search_show),

    url(r'^person_relation_search_index/',person_relation_search_index),
    url(r'^person_relation_search_show/',person_relation_search_show),

    url(r'^book_search_index/', book_search_index),
    url(r'^book_search_show/', book_search_show),
    url(r'^book_search_home/', book_search_home),

    url(r'^job_search_index/', job_search_index),
    url(r'^job_search_show/', job_search_show),
    url(r'^job_search_result/', job_search_result),

    url(r'^word_search_index/', word_search_index),
    url(r'^word_search_show/', word_search_show),

    url(r'^novel_search_index/', novel_search_index),
    url(r'^author_search_show/', author_search_show),
    url(r'^author_search_index/', author_search_index),
    url(r'^novel_book_search_index/', novel_book_search_index),
    url(r'^novel_book_search_show/', novel_book_search_show),
    url(r'^novel_type_search_index/', novel_type_search_index),
    url(r'^novel_type_search_show/', novel_type_search_show),
    url(r'^novel_type_search_result/', novel_type_search_result),
    url(r'^novel_book_search_result/', novel_book_search_result),
    url(r'^author_search_result/', author_search_result)
    ]
