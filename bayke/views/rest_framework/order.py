#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :order.py
@说明    :订单相关接口
@时间    :2023/04/25 08:50:13
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import mixins

from bayke.permissions import IsOwnerAuthenticated
# from bayke.views.rest_framework.serializers import BaykeOrderCreateSerializer
from bayke.models.order import BaykeOrder, BaykeOrderSKU
from bayke.payment.payMony import OrderPayMony, computed


############################# 序列化 ###############################

class BaykeOrderSerializer(serializers.ModelSerializer):
    """ 订单序列化基类 """
    class Meta:
        model = BaykeOrder
        exclude = ("site", "is_del")


class BaykeCreateOrderSerializer(BaykeOrderSerializer):
    """ 创建订单 """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    def create(self, validated_data):
        return super().create(validated_data)


class BaykeOrderSKUSerializer(serializers.ModelSerializer):
    """ 订单商品序列化 """
    class Meta:
        model = BaykeOrderSKU
        exclude = ("site", "is_del")
    

class BaykeCreateOrderSKUSerializer(BaykeCreateOrderSerializer):
    """ 订单详情页创建订单商品 """
    baykeordersku_set = BaykeOrderSKUSerializer(many=True, required=True)
    order_sn = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeOrder
        fields = ("id", "order_sn", "total_amount", "order_mark", "name", "phone", "email", "address", "baykeordersku_set")
    
    def update(self, instance, validated_data):
        ordersku_set = validated_data.pop("baykeordersku_set")
        # 创建商品快照
        for ordersku in ordersku_set:
            ordersku["title"] = ordersku["sku"].spu.title
            ordersku["options"] = list(ordersku["sku"].options.values("spec__name", "name"))
            ordersku["price"] = ordersku["sku"].price
            ordersku["content"] = ordersku["sku"].spu.content
            item_skus = BaykeOrderSKU.objects.filter(sku=ordersku["sku"], order=instance)
            if item_skus.exists():
                item_skus.update(**ordersku)
            else:
                BaykeOrderSKU.objects.create(**ordersku)
        # 粗略计算商品价位，未包含运费，运费需要单独运算
        paymony = OrderPayMony(instance)
        validated_data["total_amount"] = computed(paymony)
        return super().update(instance, validated_data)

############################# 视图 ###############################

class BaykeOrderViewMixin(GenericAPIView):
    """ 订单视图公共类 """
    
    serializer_class = BaykeCreateOrderSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsOwnerAuthenticated]
    queryset = BaykeOrder.objects.all()


class BaykeCreateOrderAPIView(mixins.CreateModelMixin, BaykeOrderViewMixin):
    """ 创建订单 """
    serializer_class = BaykeCreateOrderSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class BaykeCreateOrderSKUAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, BaykeOrderViewMixin):
    """ 订单详情视图关联创建订单sku """
    
    lookup_field = "order_sn"
    serializer_class = BaykeCreateOrderSKUSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)