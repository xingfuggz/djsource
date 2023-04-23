#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :token.py
@说明    :JWT登录token相关
@时间    :2023/04/23 11:35:06
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView, 
    TokenRefreshView, 
    TokenVerifyView
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from bayke.views.rest_framework.serializers import UserSerializer


def get_tokens_for_user(user):
    """ 手动获取令牌 """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):  
    
    """ 登录获取令牌 """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access_expire'] = refresh.access_token.payload['exp']   # token过期时间戳
        data['refresh_expire'] = self.get_refresh_expire()            # 刷新taoken的过期时间
        data['userinfo'] = UserSerializer(self.user, many=False).data # 用户信息
        return data
    
    def get_refresh_expire(self):
        import time
        from django.utils import timezone
        refresh_date = api_settings.REFRESH_TOKEN_LIFETIME + timezone.now()
        return int(time.mktime(time.localtime(refresh_date.timestamp())))  # 刷新taoken的过期时间戳
    
    
class TokenObtainPairView(BaseTokenObtainPairView):
    
    serializer_class = TokenObtainPairSerializer