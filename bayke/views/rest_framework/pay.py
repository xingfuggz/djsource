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
from bayke.payment.payMethod import AlipayConcreate, client



class BaykeOrderPaySerializer(BaykeOrderSerializer):
    """ 订单支付序列化 """
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
        if obj.pay_method == 2:
            return client(AlipayConcreate(obj))
        else:
            return "暂不支持该支付方式！"
        

class BaykePayOrderAPIView(RetrieveUpdateAPIView):
    """ 订单支付接口 """
    serializer_class = BaykeOrderPaySerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsOwnerAuthenticated]
    queryset = BaykeOrder.objects.all()
    lookup_field = "order_sn"
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
