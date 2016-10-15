#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from fb_echobot import views 

urlpatterns = patterns(
    # Examples:
    # url(r'^$', 'chatbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebookcheck/?$',views.fb.as_view(),name="chatbot"),
    url(r'^blog$',"views.blog",name="blog"),
)
