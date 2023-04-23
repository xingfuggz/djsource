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
from bayke.views.rest_framework import token

app_name = "bayke"

urlpatterns = [
    # 当前登录用户详情
    path('user/<int:pk>/', generics.BaykeUserRetrieveAPIView.as_view(), name='user-detail'),
    # 获取邮箱验证码
    path('obtain/code/', generics.BaykeVerifyCodeObtainAPIView.as_view(), name='obtain-code'),
    # 效验邮箱验证码
    path('check/code/', generics.BaykeVerifyCodeCheckAPIView.as_view(), name='check-code'),
    # 获取token
    path("token/", token.TokenObtainPairView.as_view(), name="token"),
    # 刷新token 
    path("refresh/", token.TokenRefreshView.as_view(), name="refresh"),
    # 验证token     
    path("verify/", token.TokenVerifyView.as_view(), name="verify"),
    # 注册接口
    path("register/", generics.BaykeUserRegisterAPIView.as_view(), name="register"),
    
    # 商品列表接口
    path("product/list/", generics.BaykeProductSPUListAPIView.as_view(), name="product-list")
]