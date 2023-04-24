from django.contrib.auth import get_user_model

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework import mixins

from bayke.models.user import BaykeUser


class CheckVerifyCodeMixin:
    """ 验证码单独效验 """
    
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        self.check_code(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
    
    def check_code(self, serializer):
        # 验证
        serializer.is_valid(raise_exception=True)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
        

class RegisterUserMixin(mixins.CreateModelMixin):
    """ 用户注册接口 """
    pass
    

class BaykeProductSPURetrieveMixin(mixins.RetrieveModelMixin):
    """ 商品详情页接口 """
    pass
    
    
class BaykeCartPushMixin(mixins.CreateModelMixin):
    """ 添加购物车 """
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    