from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

from bayke.conf import bayke_settings
from bayke.models.sites import BaykeMenu, BaykePermission


MENUS = (
    bayke_settings.ADMIN_MENUS_DATAS or 
    [
        {
            'name': '订单',
            'sort': 3,
            'icon': '',
            'perms': [{'name': '订单管理', 'codename': 'view_baykeorder', 'icon': ''}]
        },
        {
            'name': '商品',
            'sort': 4,
            'icon': '',
            'perms':[
                {'name': '商品分类', 'codename': 'view_baykeproductcategory', 'icon': ''},
                {'name': '商品规格', 'codename': 'view_baykeproductspec', 'icon': ''},
                {'name': '商品管理', 'codename': 'view_baykeproductspu', 'icon': ''}, 
                {'name': '轮播图', 'codename': 'view_baykebanner', 'icon': ''}
            ]
        },
        {
            'name': '认证和授权',
            'sort': 1,
            'icon': '',
            'perms': [
                {'name': '组', 'codename': 'view_group', 'icon': ''}, 
                {'name': '用户', 'codename': 'view_user', 'icon': ''}, 
                {'name': '菜单', 'codename': 'view_baykemenu', 'icon': ''}, 
                {'name': '日志', 'codename': 'view_logentry', 'icon': ''}
            ]
        },
        {
            'name': '内容',
            'sort': 2,
            'icon': '',
            'perms': [
                {'name': '文章分类', 'codename': 'view_baykearticlecategory', 'icon': ''}, 
                {'name': '内容管理', 'codename': 'view_baykearticle', 'icon': ''}
            ]
        }
    ]
)


class Command(BaseCommand):
    
    help = '创建后台自定义菜单'
    menus = MENUS
    
    def add_arguments(self, parser) -> None:
        pass
        # parser.add_argument(
        #     "--delete",
        #     action="store_true",
        #     help="Delete poll instead of closing it",
        # )
        
    def handle(self, *args, **options):
        if not isinstance(MENUS, (list, tuple)):
            self.stdout.write(self.style.ERROR(f'MENUS的值为{MENUS}，不可迭代，应该为list或tuple类型'))
        for menu in self.menus:
            try:
                m, c = BaykeMenu.objects.update_or_create(name=menu['name'], defaults={'name': menu['name'], 'sort': menu['sort'], 'icon': menu['icon']})
                for perm in menu['perms']:
                    perm_obj = Permission.objects.get(codename=perm['codename'])
                    BaykePermission.objects.update_or_create(permission=perm_obj, menus=m, defaults={'permission': perm_obj, 'name': perm['name'], 'icon': perm['icon']})
                    message = "创建" if c else "更新"
                    self.stdout.write(self.style.SUCCESS(f'{menu["name"]}-菜单{message}成功！'))
            except KeyError:
                self.stdout.write(self.style.ERROR(f'相关键不存在,请检查格式'))