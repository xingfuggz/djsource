#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :_create_cate.py
@说明    :创建分类相关数据
@时间    :2023/04/23 14:56:57
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''



from bayke.models.product import (
    BaykeProductCategory, BaykeProductSpec, BaykeProductSpecOption, BaykeProductSPU
)
from bayke.utils import code_random

model_name = "bayke"

CATES_DATA = [
    {
        'name': f'{model_name}-分类{code_random(2)}',
        'childrens': [
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
        ]
    },
   {
        'name': f'{model_name}-分类{code_random(2)}',
        'childrens': [
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
        ]
    },
   {
        'name': f'{model_name}-分类{code_random(2)}',
        'childrens': [
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
        ]
    },
   {
        'name': f'{model_name}-分类{code_random(2)}',
        'childrens': [
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
        ]
    },
   {
        'name': f'{model_name}-分类{code_random(2)}',
        'childrens': [
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
            {'name': f'{model_name}-分类{code_random(2)}'},
        ]
    },
]


def create_cates(model=BaykeProductCategory):
    for data in CATES_DATA:
        cate = model.objects.create(name=data['name'])
        for sub in data['childrens']:
            model.objects.create(parent=cate, name=sub['name'])
            
            
SPECS_DATA = [
    {
        'name': f'颜色',
        'childrens': [
            {'name': f'颜色{code_random(2)}'},
            {'name': f'颜色{code_random(2)}'},
            {'name': f'颜色{code_random(2)}'},
        ]
    },
    {
        'name': f'大小',
        'childrens': [
            {'name': f'大{code_random(2)}'},
            {'name': f'中{code_random(2)}'},
            {'name': f'小{code_random(2)}'},
        ]
    },
]

def create_specs():
    for data in SPECS_DATA:
        spec = BaykeProductSpec.objects.create(name=data['name'])
        for op in data['childrens']:
            BaykeProductSpecOption.objects.create(spec=spec, name=op['name'])
            


SPUS_DATA = [
    {
        'title': f'商品标题{code_random(2)}',
        'content':f'商品详情{code_random(8)}',
        'pic':f'https://demo26.crmeb.net/uploads/attach/2022/04/20220401/small_1601eee5c3b689341675b13f5e0500a2.jpg',
        'freight': code_random(1),
    },
    {
        'title': f'商品标题{code_random(2)}',
        'content':f'商品详情{code_random(8)}',
        'pic':f'http://demo26.crmeb.net/uploads/attach/2020/10/14/4b4bcc1dd6e3b310ad8c73ffa0285340.jpg',
        'freight': code_random(1),
    },
    {
        'title': f'商品标题{code_random(2)}',
        'content':f'商品详情{code_random(8)}',
        'pic':f'https://demo26.crmeb.net/uploads/attach/2021/11/20211113/big_3da27c9e0f57d6dbfd235e1ddfd7eb5a.png',
        'freight': code_random(1),
    }
]

def create_spu():
    from random import sample
    cates = BaykeProductCategory.objects.filter(parent__isnull=True).values_list('id', flat=True)
    r_cates = sample(list(cates), 2)
    for data in SPUS_DATA:
        spu = BaykeProductSPU()
        spu.title = data['title']
        spu.content = data['content']
        spu.pic = data['pic']
        spu.freight = data['freight']
        # spu.cates.set(r_cates)
        spu.save()
        # spu.cates_set.add(r_cates)
    