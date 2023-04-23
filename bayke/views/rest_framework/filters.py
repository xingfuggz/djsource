#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :filters.py
@说明    :筛选
@时间    :2023/04/23 20:21:29
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django_filters.rest_framework import FilterSet

from bayke.models.product import BaykeProductSPU, BaykeProductCategory


class BaykeProductSPUFilter(FilterSet):
    """ SPU按分类筛选 """
    
    class Meta:
        model = BaykeProductSPU
        fields = ('cates', )
    
    def filter_queryset(self, queryset):
        query = self.request.query_params
        if query.getlist('cates'):
            cate_parent = BaykeProductCategory.objects.filter(id__in=[int(i) for i in query.getlist('cates')], parent__isnull=True)
            if cate_parent.exists():
                sub_ids = []
                for cate in cate_parent:
                    sub_ids += list(cate.baykeproductcategory_set.values_list('id', flat=True))
                # 这里返回顶级分类所有的下级商品
                return BaykeProductSPU.objects.filter(cates__in=sub_ids).distinct()
        return super().filter_queryset(queryset)

