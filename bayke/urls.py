#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :urls.py
@说明    :接口url
@时间    :2023/04/22 20:32:35
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.urls import path
from bayke.views.rest_framework import generics


app_name = "bayke"

urlpatterns = [
    path('user/<int:pk>/', generics.BaykeUserRetrieveAPIView.as_view(), name='user-detail'),
    path('user/created/code/', generics.BaykeVerifyCodeCreateAPIView.as_view(), name='user-created-code'),
]