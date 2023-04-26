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


class OrderPayBase:
    """ 基类 """
    
    def computed(self) -> str:
        pass


class OrderPayMony(OrderPayBase):
    """ 订单商品的基础价位 """

    def __init__(self, order) -> None:
        self._order = order
        
    def _get_order_skus(self):
        # 订单关联商品
        return self.order.baykeordersku_set.all()

    def _get_order_skus_sum_price(self):
        """ 订单商品的单价*数量计算
        """
        return sum([(sku.price * sku.count) for sku in self._get_order_skus()])
    
    def _get_order_freight(self):
        """ 运费
        """
        freight = self._get_order_skus().values("sku__spu__freight")
        return freight.first().get("sku__spu__freight", 0)

    def _get_amount(self):
        return self._get_order_skus_sum_price()+self._get_order_freight()
    
    def computed(self) -> Decimal:
        return self._get_amount()
    
    @property
    def order(self):
        return self._order
    

class Decorator(OrderPayBase):
    """ 装饰者 """
    
    _component: OrderPayBase = None

    def __init__(self, component: OrderPayBase) -> None:
        self._component = component

    @property
    def component(self) -> OrderPayBase:
        return self._component
    
    def computed(self) -> Decimal:
        return self._component.computed()


class VIPPayMony(Decorator):
    """ VIP价位运算 """
    
    def computed(self) -> Decimal:
        pass
    
    
class CouponDeductPayMony(Decorator):
    """ 优惠券价位运算 """
    
    def computed(self) -> Decimal:
        pass


def computed(orderpay:OrderPayBase):
    """ 返回最终结果的工厂函数 """
    return orderpay.computed()