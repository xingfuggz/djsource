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

from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from rest_framework.response import Response


from bayke.permissions import IsOwnerAuthenticated
from bayke.models.order import BaykeOrder
from bayke.views.rest_framework.order import BaykeOrderSerializer
from bayke.payment.payMethod import AlipayConcreate, BalanceConcreate, client, AliPayProduct


class BaykeOrderPaySerializer(BaykeOrderSerializer):
    """ 订单支付序列化 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_sn = serializers.ReadOnlyField()
    pay_method = serializers.ChoiceField(BaykeOrder.PayMethodChoices.choices)
    total_amount = serializers.ReadOnlyField()
    pay_status = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeOrder
        fields = ("id", "owner", "order_sn", "total_amount", "pay_method", "pay_status")
        
    def validate(self, attrs):
        super().validate(attrs)
        if attrs['pay_method'] not in [2, 4]:
            raise serializers.ValidationError("暂不支持该支付方式...")
        elif not self.instance.baykeordersku_set.exists():
            raise serializers.ValidationError("该订单未关联任何商品, 请先调用向订单添加商品接口关联需要购买的商品！")
        elif self.instance.pay_status in [2,3,4,5]:
            raise serializers.ValidationError("该订单已支付，无需重复支付！")
        return attrs
    

class BaykePayOrderAPIView(RetrieveUpdateAPIView):
    """ 订单支付接口 """
    serializer_class = BaykeOrderPaySerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsOwnerAuthenticated]
    queryset = BaykeOrder.objects.all()
    lookup_field = "order_sn"
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.data['pay_method'] == 2:
            response.data['pay_url'] = client(AlipayConcreate(self.get_object()))
        elif response.data['pay_method'] == 4:
            return client(BalanceConcreate(self.get_object()))
        return response


class NotifyMixin:
    """ 支付宝post回调 """
    def notify(self, request, *args, **kwargs):
        datas = request.data.dict()
        signature = datas.pop("sign")
        order_sn = datas.get('out_trade_no')
        trade_no = datas.get('trade_no')
        orders = self.get_queryset().filter(order_sn=order_sn)
        
        success = AliPayProduct.alipay().verify(datas, signature)
        from django.utils import timezone
        if success:
            orders.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
       
        return Response("success")
    

class ReturnMixin:
    """ get回调 """
    def returner(self, request, *args, **kwargs):
        datas = request.query_params.dict()
        signature = datas.pop("sign")
        order_sn = datas.get('out_trade_no')
        trade_no = datas.get('trade_no')
        orders = self.get_queryset().filter(order_sn=order_sn)
        success = AliPayProduct.alipay().verify(datas, signature)
        from django.utils import timezone
        if success:
            orders.update(
                pay_status=2, 
                trade_sn=trade_no, 
                pay_time=timezone.now(),
                pay_method=2
            )
        
        instance = orders.first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class AliPayNotifyAPIView(NotifyMixin, ReturnMixin, GenericAPIView):
    """ 支付宝支付回调 """
    serializer_class = BaykeOrderSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsOwnerAuthenticated]
    queryset = BaykeOrder.objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.returner(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.notify(request, *args, **kwargs)