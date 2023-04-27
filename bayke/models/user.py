#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :user.py
@说明    :用户相关模型
@时间    :2023/04/21 12:30:47
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from . import base
from bayke.conf import bayke_settings


class BaykeUser(base.BaseModelMixin):
    """Model definition for BaykeUser."""
    
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name=_('用户'))
    name = models.CharField(_('姓名'), max_length=50)
    phone = models.CharField(_('手机号'), max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(_('邮箱'), max_length=254, unique=True, null=True, blank=True, editable=False)
    avatar = models.ImageField(_('头像'), upload_to='avatar/', max_length=200, blank=True, default="avatar/default.png")
    balance = models.DecimalField(_("余额"), max_digits=8, decimal_places=2, blank=True, default=0)
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeUser."""
        ordering = ['-add_date']
        verbose_name = 'BaykeUser'
        verbose_name_plural = 'BaykeUsers'

    def __str__(self):
        """Unicode representation of BaykeUser."""
        return self.owner.get_username()
    
    def save(self, *args, **kwargs):
        if self.owner.email:
            self.email = self.owner.email
        super().save(*args, **kwargs)


class BaykeVerifyCode(base.BaseModelMixin):
    """Model definition for VerifyCode."""
    
    email = models.EmailField(_("邮箱"), max_length=254)
    code = models.CharField(_("验证码"), max_length=bayke_settings.CODE_LENGTH, blank=True, default="")
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for VerifyCode."""
        ordering = ['-add_date']
        verbose_name = 'VerifyCode'
        verbose_name_plural = 'VerifyCodes'

    def __str__(self):
        """Unicode representation of VerifyCode."""
        return f"{self.email}-{self.code}"
    
    def save(self, *args, **kwargs) -> None:
        from bayke.utils import code_random
        if not self.code:
            self.code = code_random()
        super().save(*args, **kwargs)
        self.save_send_main(self.code)
    
    def save_send_main(self, code):
        from django.core.mail import send_mail
        send_mail(
            subject="BaykeShop验证码, 请查收！", 
            message=f"您的验证码为：{code}, 请尽快验证，5分钟内有效！",
            from_email="2539909370@qq.com",
            recipient_list=[self.email],
            fail_silently=False,
            auth_user="2539909370@qq.com",
            auth_password="fhrygoqlndmxebjf"
        )
        

class BaykeUserBalanceLog(base.BaseModelMixin):
    """ 用户余额变动表 """
    
    class BalanceChangeStatus(models.IntegerChoices):
        # 收支状态
        ADD = 1, _('增加')
        MINUS = 2, _('支出')
    
    class BalanceChangeWay(models.IntegerChoices):
        # 收支渠道或方式
        PAY = 1, _('线上充值')        
        ADMIN = 2, _('管理员手动更改') 
        SHOP = 3, _('余额抵扣商品')
    
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="用户")
    amount = models.DecimalField("金额", max_digits=15, decimal_places=2)
    change_status = models.PositiveSmallIntegerField(
        choices=BalanceChangeStatus.choices, 
        blank=True,
        null=True
    )
    change_way = models.PositiveSmallIntegerField(
        choices=BalanceChangeWay.choices, 
        default=BalanceChangeWay.ADMIN        # 默认为后台
    )

    class Meta:
        verbose_name = '余额明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.owner.username}-{self.amount}"