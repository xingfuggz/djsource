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

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from bayke.permissions import IsOwnerAuthenticated
from bayke.models.order import BaykeOrder
from bayke.views.rest_framework.serializers import BaykeOrderSerializer
from bayke.payment.payMethod import AlipayConcreate, BalanceConcreate, client



class BaykeOrderPaySerializer(BaykeOrderSerializer):
    """ 订单支付序列化 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.ReadOnlyField()
    pay_method = serializers.ChoiceField(BaykeOrder.PayMethodChoices.choices)
    total_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeOrder
        fields = ("id", "owner", "order_sn", "total_amount", "pay_method")
    
    def validate_pay_method(self, method):
        if method != 2:
            raise serializers.ValidationError("暂不支持该支付方式...")   
        return method
    
    def update(self, instance, validated_data):
        if not instance.baykeordersku_set.exists():
            raise serializers.ValidationError("该订单未关联任何商品")
        return super().update(instance, validated_data)
        

class BaykePayOrderAPIView(RetrieveUpdateAPIView):
    """ 订单支付接口 """
    serializer_class = BaykeOrderPaySerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsOwnerAuthenticated]
    queryset = BaykeOrder.objects.all()
    lookup_field = "order_sn"
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['pay_url'] = "asdasd"
        return response
