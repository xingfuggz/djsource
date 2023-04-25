from __future__ import annotations
from abc import ABC, abstractmethod

from django.conf import settings

from bayke.payment.alipay import AliPay
from bayke.conf import bayke_settings


class Creator(ABC):
    """ 工厂类 """
    
    @abstractmethod
    def factory_method(self):
        # 创建者
        pass
    
    def some_operation(self):
        product = self.factory_method()
        return product.operation()


class AlipayConcreate(Creator):
    """ 支付宝支付 工厂"""
    
    def factory_method(self)  -> Product:
        return AliPayProduct()


class WXPayConcreate(Creator):
    """ 微信支付 工厂"""
    
    def factory_method(self) -> Product:
        return WXPayProduct()
    
    
class Product(ABC):
    """ 抽象产品 """
    
    @abstractmethod
    def operation(self) -> str:
        pass
    

class AliPayProduct(Product):
    """ 支付宝支付的具体实现 """
    
    # 私钥
    with open(settings.BASE_DIR / bayke_settings.ALIPAY_PRIVATE_KEY, 'r') as f:
        private_key_string = f.read()
    
    # 支付宝公钥
    with open(settings.BASE_DIR / bayke_settings.ALIPAY_PUBLIC_KEY, 'r') as f:
        public_key_string = f.read()
    
    def operation(self) -> str:
        return "支付宝支付地址"
    
    @staticmethod
    def alipay():
        """ 静态方法 """
        return AliPay(
            appid=bayke_settings.ALIPAY_APPID,
            app_notify_url=bayke_settings.ALIPAY_NOTIFY_URL,
            app_private_key_string=AliPayProduct.private_key_string,
            alipay_public_key_string=AliPayProduct.public_key_string,
            sign_type=bayke_settings.ALIPAY_SIGN_TYPE,
            debug=settings.DEBUG,
            verbose=settings.DEBUG
        )
    
    
    
    
class WXPayProduct(Product):
    
    """ 微信支付的具体实现 """
    
    def operation(self) -> str:
        return "微信支付地址"


def client(creator:Creator):
    return creator.some_operation()