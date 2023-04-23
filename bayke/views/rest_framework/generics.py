#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :generics.py
@说明    :接口视图组合
@时间    :2023/04/22 17:00:42
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


from bayke.models.user import BaykeVerifyCode
from bayke.views.rest_framework.serializers import (
    UserSerializer, CreateEmailCodeSerializer
)


class BaykeUserRetrieveAPIView(RetrieveAPIView):
    """
    当前登录用户仅可查看自己的个人信息 
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)
    

class BaykeVerifyCodeCreateAPIView(CreateAPIView):
    """ 修改邮箱地址接口 """
    
    serializer_class = CreateEmailCodeSerializer
    
    def get_queryset(self):
        return BaykeVerifyCode.objects.all()
    
    
    

