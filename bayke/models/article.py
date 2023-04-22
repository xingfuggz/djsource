#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :article.py
@说明    :文章类模型
@时间    :2023/04/20 18:37:23
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import base


class BaykeArticleCategory(base.CategoryMixin):
    """Model definition for BaykeArticleCategory."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeArticleCategory."""

        verbose_name = 'BaykeArticleCategory'
        verbose_name_plural = 'BaykeArticleCategorys'

    def __str__(self):
        """Unicode representation of BaykeArticleCategory."""
        return self.name


class BaykeArticleTag(base.BaseModelMixin):
    """Model definition for BaykeArticleTag."""
    name = models.CharField(_("标签名"), max_length=50)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeArticleTag."""

        verbose_name = 'BaykeArticleTag'
        verbose_name_plural = 'BaykeArticleTags'

    def __str__(self):
        """Unicode representation of BaykeArticleTag."""
        return self.name
    

class BaykeArticle(base.ArticleMixin):
    """Model definition for BaykeArticle."""
    category = models.ForeignKey(BaykeArticleCategory, on_delete=models.CASCADE, verbose_name=_("文章分类"))
    tags = models.ManyToManyField(BaykeArticleTag, blank=True, verbose_name=_("标签"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeArticle."""
        ordering = ['-add_date']
        verbose_name = 'BaykeArticle'
        verbose_name_plural = 'BaykeArticles'

    def __str__(self):
        """Unicode representation of BaykeArticle."""
        return self.title
    
    def save(self, *args, **kwargs):
        from django.utils.html import strip_tags
        if not self.desc:
            self.desc = strip_tags(self.content)[:135]
        super().save(*args, **kwargs)

    def get_next_article(self):
        # 下一篇
        try:
            return self.get_next_by_add_date()
        except BaykeArticle.DoesNotExist:
            pass
    
    def get_previous_article(self):
        # 上一篇
        try:
            return self.get_previous_by_add_date()
        except BaykeArticle.DoesNotExist:
            pass
    