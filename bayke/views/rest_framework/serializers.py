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

from bayke.models.user import BaykeUser, BaykeVerifyCode


class BaykeUserSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeUser
        exclude = ("add_date", "pub_date")
        

class UserSerializer(serializers.ModelSerializer):
    
    username = serializers.ReadOnlyField()
    baykeuser = BaykeUserSerializer(many=False, read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'baykeuser')
        

class CreateEmailCodeSerializer(serializers.ModelSerializer):
    """ 邮箱发送验证码 """
    
    email = serializers.EmailField(
        label="邮箱", 
        max_length=150, 
        min_length=3, 
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(), 
                message="该邮箱已经存在！"
            )
        ]
    )
    code = serializers.ReadOnlyField()

    class Meta:
        model = BaykeVerifyCode
        fields = ('email', 'code')

    def create(self, validated_data):
        data = validated_data
        import datetime
        from django.utils import timezone
        from django.db.models import F
        from bayke.utils import code_random

        code = BaykeVerifyCode.objects.filter(email=data['email']).first()

        if code:
            nd = timezone.now() - datetime.timedelta(seconds=60)
            if nd > code.pub_date:
                code.code = code_random()
                code.save()
        else:
            code = BaykeVerifyCode.objects.create(email=data['email']) 
                
        return code
