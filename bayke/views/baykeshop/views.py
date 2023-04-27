#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :PC商城视图
@时间    :2023/04/27 17:37:00
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication

from bayke.models.product import BaykeProductCategory


class HomeView(mixins.ListModelMixin, GenericAPIView):
    
    queryset = BaykeProductCategory.objects.filter(parent__isnull=True, is_nav=True)
    # serializer_class = HomeBaykeCategorySerializer
    renderer_classes = (TemplateHTMLRenderer)
    authentication_classes = (SessionAuthentication)