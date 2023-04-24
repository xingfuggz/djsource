#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :pay_mony.py
@说明    :订单支付金额计算
@时间    :2023/04/24 16:10:50
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from decimal import Decimal
from . import decorator


class OrderPayAmount:

    def __init__(self, ) -> None:
        pass


class OrderPayMony(decorator.ConcreteComponent):
    
    """ 计算订单的基础价 """
    
    def _get_order_skus(self):
        # 订单关联商品
        return self.order.baykeordersku_set.all()
    
    def _get_order_skus_sum_price(self):
        # from django.db.models import Sum
        # self._get_order_skus().aggregate(Sum("price")).get("price__sum", 0)
        return sum([(sku.price * sku.count) for sku in self._get_order_skus()])
    
    def _get_order_freight(self):
        freight = self._get_order_skus().values("sku__spu__freight")
        return freight.first().get("sku__spu__freight", 0)
    
    def _get_amount(self):
        return self._get_order_skus_sum_price()+self._get_order_freight()
    
    def get_amount(self):
        return round(Decimal(self._get_amount()), 2)
    
    def operation(self) -> Decimal:
        return super().operation()