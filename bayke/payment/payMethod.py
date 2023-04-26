from __future__ import annotations
from abc import ABC, abstractmethod

from django.conf import settings

from bayke.payment import AliPay
from bayke.conf import bayke_settings
from bayke.models.order import BaykeOrder


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
    
    def __init__(self, order:BaykeOrder) -> None:
        self._order = order
    
    def factory_method(self)  -> Product:
        return AliPayProduct(self._order)


class WXPayConcreate(Creator):
    """ 微信支付 工厂"""
    
    def factory_method(self) -> Product:
        return WXPayProduct()
    
    
class Product(ABC):
    """ 抽象产品 """
    
    def __init__(self, order:BaykeOrder) -> None:
        self._order:BaykeOrder = order
    
    @abstractmethod
    def operation(self) -> str:
        pass
    
    @property
    def order(self):
        return self._order
    

class AliPayProduct(Product):
    """ 支付宝支付的具体实现 """
    
    # 私钥
    with open(settings.BASE_DIR / bayke_settings.ALIPAY_PRIVATE_KEY, 'r') as f:
        private_key_string = f.read()
    
    # 支付宝公钥
    with open(settings.BASE_DIR / bayke_settings.ALIPAY_PUBLIC_KEY, 'r') as f:
        public_key_string = f.read()
    
    @staticmethod
    def alipay():
        """ 静态方法 """
        return AliPay(
            appid=bayke_settings.ALIPAY_APPID,
            app_notify_url="http://127.0.0.1:3000",
            app_private_key_string=AliPayProduct.private_key_string,
            alipay_public_key_string=AliPayProduct.public_key_string,
            sign_type=bayke_settings.ALIPAY_SIGN_TYPE,
            debug=settings.DEBUG,
            verbose=settings.DEBUG
        )
        
    def biz_content(self):
        alipay = AliPayProduct.alipay()
        url_params = alipay.client_api(
            api_name="alipay.trade.page.pay",
            biz_content={
                "out_trade_no": self.order.order_sn,
                "total_amount": self.order.total_amount.to_eng_string(),
                "subject": self.order.order_sn,
                "product_code": "FAST_INSTANT_TRADE_PAY",
            },
            return_url="http://127.0.0.1:3000"
            # notify_url="http://127.0.0.1:3000"
        )
        return url_params
    
    def operation(self) -> str:
        """ 最终返回支付宝的支付地址 """
        alipay_api = AliPayProduct.alipay()
        import urllib.parse
        urllib.parse.unquote(self.biz_content())
        print(urllib.parse.unquote(self.biz_content()), 'asdasdas')
        # https://openapi.alipaydev.com/gateway.do?app_id=2021000116697536&biz_content=%7B%22subject%22%3A%2220230425021255168%22%2C%22out_trade_no%22%3A%2220230425021255168%22%2C%22total_amount%22%3A%22247.00%22%2C%22product_code%22%3A%22FAST_INSTANT_TRADE_PAY%22%7D&charset=utf-8&method=alipay.trade.page.pay%C2%ACify_url%3Dhttp%3A%2F%2F127.0.0.1%3A3000&return_url=http%3A%2F%2F127.0.0.1%3A3000&sign_type=RSA2%C3%97tamp%3D2023-04-26+12%3A51%3A09&version=1.0&sign=UwG1jqw%2FfQQMymKFi2Wou3P0sXTVpLyRwuXbbQIyqKS1QJrpzNkB6CV6ihujLQfUazr5vitnbXgI7wOpGyOwCunW%2BUsUd9QlKd%2FU3UatNOhBGpcznSw9ofytTKRU7ZkPuLVA1sx%2BLJABlozgi5uQCrZYVaam%2FcZQNp4JlIRMoYsmGeW0i6ItIfjJmpKlQp6RgBvmhPnvg4fWUIC09x4%2FcinLPTq73Bg2wlVPzsz4sGliQL2K8yfnKEDvP3y0k%2Fg%2BXucPY2XRgMvyY%2B55lPLA7vWE2rBguxanfnpaJ82VaypU3gBUUayCPtwRr8wyX1%2Bka19OFKgHdUCNlQROoidgTg%3D%3D
        
        # return "https://openapi-sandbox.dl.alipaydev.com/gateway.do?{data}".format(data=self.biz_content())
        return "https://openapi.alipay.com/gateway.do?{data}".format(data=self.biz_content())
    
    
class WXPayProduct(Product):
    
    """ 微信支付的具体实现 """
    
    def operation(self) -> str:
        return "微信支付地址"


def client(creator:Creator):
    return creator.some_operation()