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


class OrderPayMony(decorator.ConcreteComponent):
    
    def get_amount(self):
        return 15
    
    def get_skus_sum_price(self):
        self.order.baykeordersku_set.all()

