#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :pay.py
@说明    :支付相关
@时间    :2023/04/25 11:11:49
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework import status

from bayke.permissions import IsOwnerAuthenticated
from bayke.models.order import BaykeOrder
from bayke.views.rest_framework.serializers import BaykeOrderSerializer
        

class BaykeOrderPaySerializer(BaykeOrderSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.ReadOnlyField()
    pay_method = serializers.ChoiceField(BaykeOrder.PayMethodChoices.choices)
    total_amount = serializers.ReadOnlyField()
    pay_url = serializers.SerializerMethodField()
    
    class Meta:
        model = BaykeOrder
        fields = ("id", "owner", "order_sn", "total_amount", "pay_method", "pay_url")
        
    def validate(self, attrs):
        if attrs["pay_method"] != 2:
            raise serializers.ValidationError("暂不支持该支付方式...")
        return super().validate(attrs)

    def get_pay_url(self, obj):
        return "asdasda"
        

class BaykePayOrderAPIView(RetrieveUpdateAPIView):
    
    serializer_class = BaykeOrderPaySerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsOwnerAuthenticated]
    queryset = BaykeOrder.objects.all()
    lookup_field = "order_sn"
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
