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
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    

class BaykeProductSPURetrieveMixin(mixins.RetrieveModelMixin):
    
    pass
    
    # def retrieve(self, request, *args, **kwargs):
    #     response = super().retrieve(request, *args, **kwargs)
    #     response.data["banners"] = self.get_banners()
    #     return response
    
    # def get_banners(self):
    #     from bayke.views.rest_framework.serializers import BaykeProductBannerSerializer
    #     serializer = BaykeProductBannerSerializer(self.get_banner_queryset(), many=True)
    #     return serializer.data
    
    # def get_banner_queryset(self):
    #     return self.get_object().baykeproductbanner_set.all()
    
    