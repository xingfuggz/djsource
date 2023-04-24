#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :signal.py
@说明    :信号
@时间    :2023/04/22 17:50:27
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from bayke.models.user import BaykeUser
from bayke.models.order import BaykeOrderSKU

User = get_user_model()

@receiver(post_save, sender=User)
def update_email(sender, instance, **kwargs):
    """ 监听修改邮箱 """
    BaykeUser.objects.filter(owner=instance).update(email=instance.email)


@receiver(post_save, sender=BaykeOrderSKU)
def sku_stock_sales_update(sender, instance, **kwargs):
    """ 订单关联商品保存成功 减库存 加销量 """
    from django.db.models import F
    sku = instance.sku
    sku.stock = F("stock") - instance.count
    sku.sales = F("sales") + instance.count
    sku.save()