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

User = get_user_model()

@receiver(post_save, sender=User)
def update_email(sender, instance, **kwargs):
    """ 监听修改邮箱 """
    BaykeUser.objects.filter(owner=instance).update(email=instance.email)
