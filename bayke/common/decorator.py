#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :ordermony.py
@说明    :计算订单金额
@时间    :2023/04/22 13:17:54
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from decimal import Decimal, getcontext

from bayke.models.order import BaykeOrder


class Component():
    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    
    def __init__(self, order:BaykeOrder or Decimal) -> None:
        self._order = order
    
    def get_amount(self):
        """ 判断初始化该类是否传了订单，或者金额 """
        amount = self._order
        if hasattr(self._order, 'total_amount'):
            amount = self._order.total_amount
        return amount
    
    def operation(self) -> Decimal:
        return self.get_amount()
    
    @property
    def order(self):
        return self._order


class Decorator(Component):
    
    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self) -> str:
        return self._component.operation()


class VIPPayMony(Decorator):
    """ 会员折扣 """
    
    def operation(self) -> Decimal:
        return round(self.component.operation() * Decimal(0.8), 2)


class CouponDeductPayMony(Decorator):
    
    """ 优惠券抵扣后的钱数 """
    
    def operation(self) -> Decimal:
        return self.component.operation() - 10


def client(component: Component) -> None:
    """
    from bayke.common import decorator
    from bayke.models.order import BaykeOrder

    simple_amount = decorator.ConcreteComponent(BaykeOrder.objects.get(order_sn="20230422060604161"))
    
    or
    
    from decimal import Decimal
    simple_amount = decorator.ConcreteComponent(Decimal(152))
    
    # vip优惠价
    vip_amount = decorator.VIPOrderPayMony(simple_amount)
    
    # 在vip的折扣基础上再用优惠券抵扣
    coupon = decorator.CouponDeductPayMony(vip_amount)
    
    # 最终返回的价格
    print(decorator.client_code(full_sub))
    """
    
    return component.operation()
