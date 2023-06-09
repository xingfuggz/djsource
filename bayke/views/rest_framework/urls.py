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
from bayke.views.rest_framework.order import BaykeCreateOrderAPIView, BaykeCreateOrderSKUAPIView
from bayke.views.rest_framework.pay import BaykePayOrderAPIView, AliPayNotifyAPIView

urlpatterns = [
    # 当前登录用户详情
    path('user/<int:pk>/', generics.BaykeUserRetrieveAPIView.as_view(), name='user-detail'),
    # 获取邮箱验证码 post
    path('obtain/code/', generics.BaykeVerifyCodeObtainAPIView.as_view(), name='obtain-code'),
    # 效验邮箱验证码 post
    path('check/code/', generics.BaykeVerifyCodeCheckAPIView.as_view(), name='check-code'),
    # 获取token post
    path("token/", token.TokenObtainPairView.as_view(), name="token"),
    # 刷新token post
    path("refresh/", token.TokenRefreshView.as_view(), name="refresh"),
    # 验证token post 
    path("verify/", token.TokenVerifyView.as_view(), name="verify"),
    # 注册接口 post
    path("register/", generics.BaykeUserRegisterAPIView.as_view(), name="register"),
    
    # 轮播图 get => list
    path('banners/', generics.BaykeBannerListAPIView.as_view(), name='banners'),
    
    # 商品列表接口 get
    path("product/list/", generics.BaykeProductSPUListAPIView.as_view(), name="product-list"), 
    # 商品详情接口 get
    path("product/<int:pk>/", generics.BaykeProductSPURetrieveAPIView.as_view(), name="product-detail"),
    
    # 加入购物车接口 get=>list  post=>create
    path("carts/", generics.BaykeCartAPIView.as_view(), name="carts"),
    # 修改购物车数量 put patch
    path("carts/<int:pk>/count/", generics.BaykeCartUpdateCountAPIView.as_view(), name="carts-update-count"),
    
    # 创建订单
    path('order/create/', BaykeCreateOrderAPIView.as_view(), name='order-create'),
    # 查看订单基础信息及创建关联商品，计算价格 get->detail put->order
    path('order/create/<str:order_sn>/', BaykeCreateOrderSKUAPIView.as_view(), name='order-create-sku'),
    
    # 支付
    path('pay/<str:order_sn>/', BaykePayOrderAPIView.as_view(), name='pay-order'),
    
    # 支付宝支付回调
    path('alipay/success/', AliPayNotifyAPIView.as_view(), name="alipay-success")
]
