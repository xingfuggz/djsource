#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :middleware.py
@说明    :中间件
@时间    :2023/04/22 18:17:25
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from bayke.models.user import BaykeUser
from django.db.utils import OperationalError


class CreateUserInfoMiddleware:
    """
    一对一关联用户默认关联中间件
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            try:
                request.user.baykeuser
            except BaykeUser.DoesNotExist:
                BaykeUser.objects.create(owner=request.user)
                
        response = self.get_response(request)
        
        return response
