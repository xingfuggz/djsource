#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :cart.py
@说明    :购物车相关模型
@时间    :2023/04/21 11:57:37
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from . import base
from . import product


class BaykeCart(base.BaseModelMixin):
    """Model definition for BaykeCart."""
    
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="用户")
    sku = models.ForeignKey(product.BaykeProductSKU, on_delete=models.CASCADE, verbose_name="规格商品")
    count = models.PositiveIntegerField(default=1, verbose_name=_("数量"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeCart."""
        ordering = ['-add_date']
        verbose_name = 'BaykeCart'
        verbose_name_plural = 'BaykeCarts'
        constraints = [
            models.UniqueConstraint(fields=['owner', 'sku'], name='unique_owner_sku')
        ]

    def __str__(self):
        """Unicode representation of BaykeCart."""
        return self.sku.spu.title
    
    @classmethod
    def get_cart_count(cls, user) -> dict: 
        # 当前用户的购物车商品数量
        from django.db.models import Sum
        return cls.objects.filter(owner=user).aggregate(Sum('count'))

    def clean(self) -> None:
        if self.count > self.sku.stock:
            raise ValueError(gettext("购车数量不能大于商品库存！"))         
        return super().clean()