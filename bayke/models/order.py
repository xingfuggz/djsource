#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :order.py
@说明    :订单相关模型
@时间    :2023/04/21 12:17:32
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _
from . import base
from . import product


class BaykeOrder(base.OrderMixin):
    """Model definition for BaykeOrder."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeOrder."""
        ordering = ['-add_date']
        verbose_name = 'BaykeOrder'
        verbose_name_plural = 'BaykeOrders'

    def __str__(self):
        """Unicode representation of BaykeOrder."""
        return self.order_sn
    
    def save(self, *args, **kwargs):
        if not self.order_sn:
            self.order_sn = self.generate_order_sn()
        super().save(*args, **kwargs)

    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        from random import Random
        from django.utils import timezone
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str = timezone.now().strftime("%Y%m%d%H%M%S"),
            user_id = self.owner.id,
            ranstr = random_ins.randint(10, 99))
        return order_sn
    

class BaykeOrderSKU(base.BaseModelMixin):
    """Model definition for BaykeOrderSKU."""
    
    order = models.ForeignKey(BaykeOrder, on_delete=models.CASCADE, verbose_name=_("订单"))
    title = models.CharField(_("商品标题"), max_length=100, editable=False)
    options = models.JSONField(_("商品规格"), editable=False)
    price = models.DecimalField(_("商品单价"), max_digits=8, decimal_places=2, editable=False)
    content = models.TextField(_("商品详情"), editable=False)
    count = models.IntegerField(default=1, verbose_name=_("数量"))
    sku = models.ForeignKey(product.BaykeProductSKU, on_delete=models.SET_NULL, blank=True, null=True)
    is_commented = models.BooleanField(default=False, verbose_name="是否已评价")

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeOrderSKU."""
        ordering = ['-add_date']
        verbose_name = 'BaykeOrderSKU'
        verbose_name_plural = 'BaykeOrderSKUs'

    def __str__(self):
        """Unicode representation of BaykeOrderSKU."""
        return self.order.order_sn
