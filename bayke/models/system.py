#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :conf.py
@说明    :配置相关模型
@时间    :2023/04/21 15:35:40
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import base


class BaykeSystemConfCategory(base.CategoryMixin):
    """Model definition for BaykeSystemConf."""
    
    class ConfTypeChoices(models.IntegerChoices):
        SYS = 0, _("系统配置")
        EXT = 1, _("额外配置")

    parent = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name=_("上级分类"))
    en_name = models.CharField(_("英文名称"), max_length=80, unique=True)
    is_show = models.BooleanField(_("是否显示"), default=True)
    conf_type = models.PositiveSmallIntegerField(
        choices=ConfTypeChoices.choices, 
        default=ConfTypeChoices.SYS, 
        verbose_name=_("配置类型")
    )
    sort = models.PositiveSmallIntegerField(_("排序"), default=1)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeSystemConf."""
        ordering = ['-sort']
        verbose_name = 'BaykeSystemConf'
        verbose_name_plural = 'BaykeSystemConfs'

    def __str__(self):
        """Unicode representation of BaykeSystemConf."""
        return self.name
    
    @classmethod
    def get_conf_cate_tree(cls):
        """ 递归分类 """
        tree = []
        def generate_tree():
            for item in cls.objects.all():
                if item.parent is None:
                    item.sub_cates = generate_tree(cls.objects.all(), item.id)
                    tree.append(item)
        return tree
    

class BaykeSystemConf(base.BaseModelMixin):
    """Model definition for BaykeSystemConf."""
    # https://doc.crmeb.com/single/crmeb_v4/1128
    class InputTypeChoices(models.IntegerChoices):
        TEXT = 0, _("文本框")
        RADIO = 1, _("单选")
        EMAIL = 2, _("邮件")
        NUMBER = 3, _("数字")
        CHECKBOX = 4, _("复选框")
        FILE = 5, _("文件")
        TEXTAREA = 6, _("多行文本")
        
    class FieldTypeChoices(models.IntegerChoices):
        INT = 0, _("数字类型")
        CHAR = 1, _("文本类型")
        BOOL = 2, _("布尔类型")
        
    cate = models.ForeignKey(BaykeSystemConfCategory, on_delete=models.CASCADE, verbose_name=_("配置分类"))
    field_name = models.CharField(_("字段名称"), max_length=50, unique=True)
    input_type = models.PositiveSmallIntegerField(default=InputTypeChoices.TEXT, verbose_name=_("表单类型"))
    field_type = models.PositiveSmallIntegerField(default=FieldTypeChoices.CHAR, verbose_name=_("字段类型"))
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeSystemConf."""

        verbose_name = 'BaykeSystemConf'
        verbose_name_plural = 'BaykeSystemConfs'

    def __str__(self):
        """Unicode representation of BaykeSystemConf."""
        return self.field_name
