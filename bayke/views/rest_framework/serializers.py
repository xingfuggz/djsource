#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :serializers.py
@说明    :序列化
@时间    :2023/04/22 17:26:05
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from bayke.conf import bayke_settings
from bayke.models.user import BaykeUser, BaykeVerifyCode


class BaykeUserSerializer(serializers.ModelSerializer):
    """ 一对一关联用户信息 """
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeUser
        exclude = ("add_date", "pub_date")
        

class UserSerializer(serializers.ModelSerializer):
    """ 用户 """
    username = serializers.ReadOnlyField()
    baykeuser = BaykeUserSerializer(many=False, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'baykeuser')
        

class ObtainEmailCodeSerializer(serializers.ModelSerializer):
    """ 邮箱发送验证码 """
    
    email = serializers.EmailField(
        label="邮箱", 
        max_length=150, 
        min_length=3
    )
    code = serializers.ReadOnlyField()

    class Meta:
        model = BaykeVerifyCode
        fields = ('email', 'code')

    def create(self, validated_data):
        data = validated_data
        from django.utils import timezone
        from bayke.utils import code_random

        code = BaykeVerifyCode.objects.filter(email=data['email']).first()

        if code:
            # nd = timezone.now() - datetime.timedelta(seconds=60)
            nd = timezone.now() - bayke_settings.EMAIL_CODE_EXP
            # 判断是否过期，刷新验证码
            if nd > code.pub_date:
                code.code = code_random()
                code.save()
            else:
                # 这里只发送邮件
                code.save_send_main(code.code)
        else:
            code = BaykeVerifyCode.objects.create(email=data['email'])     
        return code


class CheckEmailCodeSerializer(serializers.Serializer):
    
    """ 验证码效验 """
    
    code = serializers.CharField(
        label="验证码", 
        max_length=bayke_settings.CODE_LENGTH, 
        min_length=bayke_settings.CODE_LENGTH
    )
    email = serializers.EmailField(label="邮箱", max_length=150)
    
    def validate(self, attrs):
        email_codes = BaykeVerifyCode.objects.filter(email=attrs['email'], code=attrs['code'])
        if not email_codes.exists():
            raise serializers.ValidationError("该验证码无效！")
        else:
            code = email_codes.first()
            from django.utils import timezone
            nd = timezone.now() - bayke_settings.EMAIL_CODE_EXP
            # 判断是否过期，刷新验证码
            if nd > code.pub_date:
                raise serializers.ValidationError("该验证码已过期，请重新获取！")
        return attrs
    