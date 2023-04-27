#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :urls.py
@说明    :PC商城url
@时间    :2023/04/27 17:35:27
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]