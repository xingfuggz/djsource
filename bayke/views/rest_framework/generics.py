#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :generics.py
@说明    :接口视图组合
@时间    :2023/04/22 17:00:42
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.generics import (
    RetrieveAPIView, CreateAPIView, GenericAPIView,
    ListAPIView, RetrieveUpdateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

from bayke.permissions import IsOwnerAuthenticated


class BaykeUserRetrieveAPIView(RetrieveAPIView):
    """ 当前登录用户仅可查看自己的个人信息 """
    from bayke.views.rest_framework.serializers import UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)
    

class BaykeVerifyCodeObtainAPIView(CreateAPIView):
    """ 获取验证码接口 """
    from bayke.views.rest_framework.serializers import ObtainEmailCodeSerializer
    serializer_class = ObtainEmailCodeSerializer
    
    def get_queryset(self):
        from bayke.models.user import BaykeVerifyCode
        return BaykeVerifyCode.objects.all()
    

from bayke.views.rest_framework.mixins import CheckVerifyCodeMixin  
class BaykeVerifyCodeCheckAPIView(CheckVerifyCodeMixin, GenericAPIView):
    """ 邮箱验证码验证是否过期或是否存在
    该接口存在的目的仅用作证明邮箱是一个可用的真实邮箱
    其他登录注册如需要邮箱验证功能仅需要在你的序列化期中
    继承CheckEmailCodeSerializer序列化器即可
    """
    from bayke.views.rest_framework.serializers import CheckEmailCodeSerializer
    serializer_class = CheckEmailCodeSerializer
    
    def post(self, request, *args, **kwargs):
        return self.verify(request, *args, **kwargs)


from bayke.views.rest_framework.mixins import RegisterUserMixin
class BaykeUserRegisterAPIView(RegisterUserMixin, GenericAPIView):
    
    """ 用户注册接口 
    这个用到了邮箱验证码验证
    """
    from bayke.views.rest_framework.serializers import RegisterSerializer
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class BaykeProductSPUListAPIView(ListAPIView):
    """ 商品列表接口 
    搜索模糊匹配： "title", "desc", "keywords", "content"
    排序：        'baykeproductsku__price', 'baykeproductsku__sales', 'add_date'
    多分类筛选:    cates=33&cates=34
    """
    from django_filters.rest_framework.backends import DjangoFilterBackend
    from bayke.models.product import BaykeProductSPU
    from bayke.views.rest_framework.serializers import BaykeProductSPUSerializer
    from bayke.views.rest_framework.filters import BaykeProductSPUFilter
    from bayke.pagination import PageNumberPagination
    
    serializer_class = BaykeProductSPUSerializer
    queryset = BaykeProductSPU.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BaykeProductSPUFilter
    search_fields = ("title", "desc", "keywords", "content")
    ordering_fields = ('baykeproductsku__price', 'baykeproductsku__sales', 'add_date',)
    

from bayke.views.rest_framework.mixins import BaykeProductSPURetrieveMixin
class BaykeProductSPURetrieveAPIView(BaykeProductSPURetrieveMixin, GenericAPIView):
    """ 商品详情页接口 """
    from bayke.models.product import BaykeProductSPU
    from bayke.views.rest_framework.serializers import BaykeProductSPUSerializer
    serializer_class = BaykeProductSPUSerializer
    queryset = BaykeProductSPU.objects.all()


###################################################################################################
# start 购物车相关接口

from bayke.views.rest_framework.mixins import BaykeCartPushMixin
class BaykeCartViewMixin:
    """ GenericAPIView 属性集合 """
    from bayke.views.rest_framework.serializers import BaykeCartSerializer
    from bayke.models.cart import BaykeCart
    serializer_class = BaykeCartSerializer
    permission_classes = [IsOwnerAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    queryset = BaykeCart.objects.all()


class BaykeCartAPIView(mixins.ListModelMixin, BaykeCartPushMixin, BaykeCartViewMixin, GenericAPIView):
    """ 查看和新增购物车 """
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BaykeCartUpdateCountAPIView(BaykeCartViewMixin, RetrieveUpdateAPIView):

    """ 修改购物车商品数量 """
    from bayke.views.rest_framework.serializers import BaykeCartUpdateCountSerializer
    serializer_class = BaykeCartUpdateCountSerializer

    # 如某些平台不支持put请求，可开启该方法，使其支持post方法
    # def post(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    
# end 购物车相关接口
###################################################################################################
