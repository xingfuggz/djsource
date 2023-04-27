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
from rest_framework.authentication import SessionAuthentication
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from bayke.models.product import BaykeProductCategory
from .serializer import BaykeProductCategorySerializer
from . import pagination


class HomeView(mixins.ListModelMixin, GenericAPIView):
    """ 首页 """
    queryset = BaykeProductCategory.objects.filter(parent__isnull=True, is_nav=True)
    serializer_class = BaykeProductCategorySerializer
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    authentication_classes = (SessionAuthentication,)
    pagination_class = pagination.HomeFloorPagination
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.template_name = "baykeshop/index.html"
        return response