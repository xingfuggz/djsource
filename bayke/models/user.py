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
        from django.core.mail import send_mail
        from bayke.utils import code_random
        if not self.code:
            self.code = code_random()
        super().save(*args, **kwargs)
        send_mail(
            subject="BaykeShop验证码, 请查收！", 
            message=f"您的验证码为：{self.code}, 请尽快验证，5分钟内有效！",
            from_email="1158920674@qq.com",
            recipient_list=[self.email],
            fail_silently=False,
            auth_user="2539909370@qq.com",
            auth_password="fhrygoqlndmxebjf"
        )
    