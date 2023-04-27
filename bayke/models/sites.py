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
from django.contrib.auth.models import Permission
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
        from django.core.exceptions import ValidationError
        if BaykeSite.objects.count():
            raise ValidationError("仅允许添加一条站点信息")
        return super().clean()


class BaykeMenu(base.CategoryMixin):
    """ 菜单 """
    sort = models.PositiveSmallIntegerField(_("排序"), default=1)

    class Meta:
        ordering = ['-sort']
        verbose_name = _('菜单')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PermMixin(base.CategoryMixin):
    """ 权限关系基类 """
    permission = models.OneToOneField(
        Permission, 
        on_delete=models.CASCADE, 
        verbose_name=_("权限"), 
        blank=True, 
        null=True
    )
    menus = models.ForeignKey(
        BaykeMenu, 
        on_delete=models.CASCADE, 
        verbose_name=_("菜单")
    )
    # TODO

    class Meta:
        abstract = True


class BaykePermission(PermMixin):
    """ 权限规则 """
    sort = models.PositiveSmallIntegerField(_("排序"), default=1)
    is_show = models.BooleanField(default=True, verbose_name=_("是否显示"))

    class Meta:
        verbose_name = _('菜单权限')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.permission.name}"
    

class BaykeBanner(base.ImageMixin):
    """Model definition for BaykeBanner."""
    place = models.CharField(
        _("位置标识"), 
        max_length=50, 
        blank=True, 
        null=True, 
        unique=True, 
        help_text=_("留空则为首页banner，否则为指定位置banner")
    )
    target_url = models.CharField(_("跳转地址"), max_length=150, blank=True, default="")
    sort = models.PositiveSmallIntegerField(_("排序"), default=1)
    # TODO: Define fields here

    class Meta(base.BaseModelMixin.Meta):
        verbose_name = _("轮播图")
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return f"{self.place}【{self.img.url}】" if self.place else f"Home Banner{self.img.url}"


class BaykeUpload(base.BaseModelMixin):
    """ 富文本编辑器图片上传 """
    img = models.ImageField(upload_to="upload/editor/", max_length=200)
    
    class Meta:
        verbose_name = '富文本编辑器图片上传'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.img.name