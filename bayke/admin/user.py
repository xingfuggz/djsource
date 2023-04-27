from django.contrib import admin
from django.contrib.auth.models import Permission, User, Group
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
    GroupAdmin as BaseGroupAdmin
)
from django.core.cache import cache
from django.utils.html import format_html

from bayke.models.sites import BaykePermission, BaykeMenu, BaykeBanner
from bayke.models.user import BaykeUser, BaykeUserBalanceLog
from bayke.admin.base import BaseModelAdmin
from bayke.admin.base import TabularInline, StackedInline

# 禁用全局删除
# admin.site.disable_action('delete_selected')

admin.site.unregister(User)
admin.site.unregister(Group)


class BaykeUserInline(StackedInline):
    '''Tabular Inline View for BaykeUserInfo'''
    model = BaykeUser
    

class BaykePermissionInline(TabularInline):
    '''Tabular Inline View for BaykePermission'''

    model = BaykePermission
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)
    exclude = ('desc', 'keywords')



@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseModelAdmin):
    inlines = (BaykeUserInline, )

    # 编辑打开之前先缓存旧值，之后保存时读取缓存并比较
    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        if obj is not None:
            user, created = BaykeUser.objects.get_or_create(
                owner=obj,
                defaults={'owner': obj},
            )
            cache.set(f'{obj.username}_balance', obj.baykeuserinfo.balance)
            # cache_balance = cache.get(f"{obj.username}_balance")
        return super().get_inline_formsets(request, formsets, inline_instances, obj)

    def save_formset(self, request, form, formset, change):
        cache_balance = cache.get(f"{form.cleaned_data['username']}_balance", 0)
        data = formset.cleaned_data[0]
        balance = data.get('balance', 0)
        
        if float(balance) > 0 and float(balance) > float(cache_balance):
            item_balance = float(balance) - float(cache_balance)
            BaykeUserBalanceLog.objects.create(
                owner=data['owner'],
                amount=item_balance,
                change_status=1,
                change_way=2
            )
        elif float(balance) < float(cache_balance) and float(balance) != 0:
            item_balance = float(cache_balance) - float(balance)
            BaykeUserBalanceLog.objects.create(
                owner=data['owner'],
                amount=item_balance,
                change_status=2,
                change_way=2
            )
        elif float(balance) == 0 and float(balance) < float(cache_balance):
            BaykeUserBalanceLog.objects.create(
                owner=data['owner'],
                amount=float(cache_balance),
                change_status=2,
                change_way=2
            )
        return super().save_formset(request, form, formset, change)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, BaseModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(BaseModelAdmin):
    '''Admin View for BaykePermission'''

    list_display = ('id', 'name',)
    search_fields = ('name', )
    readonly_fields = ('codename', 'content_type')
    inlines = (BaykePermissionInline, )


@admin.register(BaykePermission)
class BaykePermissionAdmin(BaseModelAdmin):
    '''Admin View for BaykePermission'''

    list_display = ('id','menus_name', 'verbose_name', 'operate')

    @admin.display(description='权限菜单')
    def permission_name(self, obj):
        return f"{obj.permission.name}"
    
    @admin.display(description='verboseName')
    def verbose_name(self, obj):
        return f"{obj.permission.content_type.model_class()._meta.verbose_name}"
    
    @admin.display(description='归属菜单')
    def menus_name(self, obj):
        return f"{obj.menus.name}"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "menus":
            kwargs["queryset"] = BaykeMenu.objects.filter(
                parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BaykeMenu)
class BaykeMenuAdmin(BaseModelAdmin):
    '''Admin View for BaykeMenu'''

    list_display = ('id', 'name', 'sort', 'operate')
    list_editable = ('sort',)
    inlines = (BaykePermissionInline, )
    exclude = ('desc', 'keywords')


@admin.register(LogEntry)
class LogEntryAdmin(BaseModelAdmin):
    '''Admin View for '''

    list_display = (
        'id', 'action_time', 'user', 'content_type',
        'object_id', 'object_repr', 'action_flag', 'change_message'
    )

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
    

@admin.register(BaykeBanner)
class BaykeShopBannerAdmin(BaseModelAdmin):
    list_display = ('id', 'imgformat', 'target_url', 'operate')
    
    @admin.display(description="轮播图")
    def imgformat(self, obj):
        return format_html(f'<img src="{obj.img.url}" width="auto" height="100px" />')

    class Media:
        css = {'all': ['bayke/css/ordersku.css']}