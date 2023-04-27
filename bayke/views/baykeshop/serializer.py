#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializer.py
@说明    :pc视图序列化
@时间    :2023/04/27 18:06:33
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from rest_framework import serializers

from bayke.models.product import BaykeProductCategory



class BaykeProductCategorySerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = BaykeProductCategory
        fields = "__all__"
    
    def get_products(self, obj):
        return []