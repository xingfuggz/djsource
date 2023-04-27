#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :product.py
@说明    :商品管理
@时间    :2023/04/23 18:03:53
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

# Register your models here.
from bayke.admin.base import BaseModelAdmin, TabularInline, StackedInline
from bayke.models import product


class BaykeProductCategoryInline(TabularInline):
    model = product.BaykeProductCategory
    min_num = 1
    max_num = 20
    extra = 1
    
    
class BaykeProductSKUInline(TabularInline):
    model = product.BaykeProductSKU
    # min_num = 1
    max_num = 20
    extra = 1
    can_delete = False
    

class BaykeProductSpecOptionInline(StackedInline):
    '''Stacked Inline View for '''

    model = product.BaykeProductSpecOption
    min_num = 1
    max_num = 20
    extra = 1


class BaykeProductBannerInline(StackedInline):
    '''Tabular Inline View for '''

    model = product.BaykeProductBanner
    min_num = 1
    max_num = 20
    extra = 1
    exclude = ('desc',)



@admin.register(product.BaykeProductCategory)
class BaykeProductCategoryAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'parent', 'operate')
    exclude = ('parent', )
    inlines = (BaykeProductCategoryInline, )
    # search_fields = ('parent__name',)
    # autocomplete_fields = ('parent', )
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = product.BaykeProductCategory.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(product.BaykeProductSPU)
class BaykeProductSPUAdmin(BaseModelAdmin):
    list_display = (
        'id', 
        'dis_cover_pic', 
        'title', 
        'dis_price', 
        # 'dis_spec', 
        'dis_sales',
        'dis_stock',
        'operate'
    )
    list_display_links = ('title', )
    filter_horizontal = ('cates',)
    inlines = (BaykeProductBannerInline, BaykeProductSKUInline, )
    
    class Media:
        css = {'all': ['bayke/css/ordersku.css']}
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'cates':
            kwargs['queryset'] = product.BaykeProductCategory.objects.filter(parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_skus(self, obj):
        return obj.baykeproductsku_set.order_by('price')
    
    @admin.display(description="封面图")
    def dis_cover_pic(self, obj):
        return format_html(mark_safe("<img width='64px' height='64px' src='{}' />"), obj.pic.url)
    
    @admin.display(description="价格")
    def dis_price(self, obj):
        return list(self.get_skus(obj).values_list('price', flat=True))
    
    # @admin.display(description="包含规格")
    # def dis_spec(self, obj):
    #     params = []
    #     for u in self.get_skus(obj):
    #         for op in u.options.all():
    #             op_dict = {
    #                 f"{op.spec.name}":f"{op.name}"
    #             }
    #             params.append(op_dict)
    #     return params
    
    @admin.display(description="销量")
    def dis_sales(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('sales'))['sales__sum']

    @admin.display(description="库存")
    def dis_stock(self, obj):
        from django.db.models import Sum
        return self.get_skus(obj).aggregate(Sum('stock'))['stock__sum']


@admin.register(product.BaykeProductSpec)
class BaykeProductSpecAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'operate')
    search_fields = ('name',)
    inlines = (BaykeProductSpecOptionInline, )
    