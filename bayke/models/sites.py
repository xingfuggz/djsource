#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :sites.py
@说明    :站点信息
@时间    :2023/04/21 12:50:22
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from . import base


class BaykeSite(base.BaseModelMixin):
    """Model definition for BaykeSite."""

    site_name = models.CharField(_("站点名称"), max_length=50, blank=True, default=_("Bayke"))
    site_title = models.CharField(_("站点标题"), max_length=50, blank=True, default=_("Bayke商城管理系统"))
    site_header = models.CharField(_("站点描述"), max_length=50, blank=True, default=_("Bayke System"))
    beian = models.CharField(_("备案信息"), max_length=200, blank=True, default="")
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeSite."""
        
        verbose_name = 'BaykeSite'
        verbose_name_plural = 'BaykeSites'

    def __str__(self):
        """Unicode representation of BaykeSite."""
        return self.site_name
    
    def save(self, *args, **kwargs):
        if not BaykeSite.objects.count():
            super().save(*args, **kwargs)
    
    def clean(self) -> None:
        if BaykeSite.objects.count():
            raise ValueError("仅允许添加一条站点信息")
        return super().clean()

