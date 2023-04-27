#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :product.py
@说明    :商品相关模型
@时间    :2023/04/20 19:43:07
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _
from . import base


class BaykeProductCategory(base.CategoryMixin):
    """Model definition for BaykeProductCategory."""

    parent = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        verbose_name=_("父级")
    )
    pic = models.ImageField(_("推荐图"), upload_to="product/cate/", max_length=200, blank=True, default="default/cate.png")
    is_nav = models.BooleanField(_("菜单推荐"), default=True)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeProductCategory."""
        ordering = ['-add_date']
        verbose_name = 'BaykeProductCategory'
        verbose_name_plural = 'BaykeProductCategorys'

    def __str__(self):
        """Unicode representation of BaykeProductCategory."""
        return self.name
    
    @classmethod
    def get_cates(cls):
        cates = cls.objects.filter(is_nav=True, parent__isnull=True)
        for cate in cates:
            cate.sub_cates = cate.baykeproductcategory_set.filter(is_nav=True)
        return cates


class BaykeProductSpec(base.BaseModelMixin):
    """Model definition for BaykeProductSpec."""

    name = models.CharField(_("规格名"), max_length=50)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeProductSpec."""
        ordering = ['-add_date']
        verbose_name = 'BaykeProductSpec'
        verbose_name_plural = 'BaykeProductSpecs'

    def __str__(self):
        """Unicode representation of BaykeProductSpec."""
        return self.name


class BaykeProductSpecOption(base.BaseModelMixin):
    """Model definition for BaykeProductSpecOption."""
    
    spec = models.ForeignKey(BaykeProductSpec, on_delete=models.CASCADE, verbose_name=_("规格"))
    name = models.CharField(_("规格值"), max_length=50)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeProductSpecOption."""
        ordering = ['-add_date']
        verbose_name = 'BaykeProductSpecOption'
        verbose_name_plural = 'BaykeProductSpecOptions'

    def __str__(self):
        """Unicode representation of BaykeProductSpecOption."""
        return self.name


class BaykeProductSPU(base.GoodsMixin):
    """Model definition for BaykeSpu."""
    
    cates = models.ManyToManyField(BaykeProductCategory, verbose_name=_("商品分类"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeSpu."""
        ordering = ['-add_date']
        verbose_name = 'BaykeSpu'
        verbose_name_plural = 'BaykeSpus'

    def __str__(self):
        """Unicode representation of BaykeSpu."""
        return self.title

    def save(self, *args, **kwargs):
        from django.utils.html import strip_tags
        if not self.desc:
            self.desc = strip_tags(self.content)[:135]
        super().save(*args, **kwargs)


class BaykeProductSKU(base.ProductMixin):
    """Model definition for BaykeProductSKU."""

    spu = models.ForeignKey(BaykeProductSPU, on_delete=models.CASCADE, verbose_name=_("商品"))
    options = models.ManyToManyField(BaykeProductSpecOption, verbose_name=_("规格值"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeProductSKU."""
        ordering = ['-add_date']
        verbose_name = 'BaykeProductSKU'
        verbose_name_plural = 'BaykeProductSKUs'

    def __str__(self):
        """Unicode representation of BaykeProductSKU."""
        return self.spu.title


class BaykeProductBanner(base.ImageMixin):
    """Model definition for BaykeProductBanner."""

    spu = models.ForeignKey(BaykeProductSPU, on_delete=models.CASCADE, verbose_name=_("商品"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeProductBanner."""
        ordering = ['-add_date']
        verbose_name = 'BaykeProductBanner'
        verbose_name_plural = 'BaykeProductBanners'

    def __str__(self):
        """Unicode representation of BaykeProductBanner."""
        return self.img.name