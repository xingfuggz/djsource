from __future__ import annotations
from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.conf import settings

from bayke.payment import AliPay
from bayke.conf import bayke_settings
from bayke.models.order import BaykeOrder



User = get_user_model()


class Creator(ABC):
    """ 工厂类 """
    
    def __init__(self, order:BaykeOrder) -> None:
        self._order = order
    
    @abstractmethod
    def factory_method(self):
        # 创建者
        pass
    
    def some_operation(self):
        product = self.factory_method()
        # return product.operation()
        return product.payment()


class AlipayConcreate(Creator):
    """ 支付宝支付 工厂"""
    
    def factory_method(self)  -> Product:
        return AliPayProduct(self._order)


class WXPayConcreate(Creator):
    """ 微信支付 工厂"""
    def factory_method(self) -> Product:
        return WXPayProduct()


class BalanceConcreate(Creator):
    
    def __init__(self, order: BaykeOrder, owner:User) -> None:
        super().__init__(order)
        self.owner = owner
    
    def factory_method(self):
        return BalanceProduct(self._order, self.owner)

    
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
    private_key_string = ""
    with open(settings.BASE_DIR / bayke_settings.ALIPAY_PRIVATE_KEY, 'r') as f:
        private_key_string = f.read()
    
    # 支付宝公钥
    public_key_string = ""
    with open(settings.BASE_DIR / bayke_settings.ALIPAY_PUBLIC_KEY, 'r') as f:
        public_key_string = f.read()
    
    @staticmethod
    def alipay():
        """ 静态方法 """
        return AliPay(
            appid=bayke_settings.ALIPAY_APPID,
            app_private_key_string=AliPayProduct.private_key_string,
            alipay_public_key_string=AliPayProduct.public_key_string,
            sign_type=bayke_settings.ALIPAY_SIGN_TYPE,
            debug=settings.DEBUG,
            verbose=settings.DEBUG,
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
            return_url="http://127.0.0.1:3000",
        )
        return url_params
    
    def operation(self) -> str:
        """ 最终返回支付宝的支付地址 """
        if settings.DEBUG:
            url = "https://openapi-sandbox.dl.alipaydev.com/gateway.do?{data}".format(data=self.biz_content())
        else:
            url = "https://openapi.alipay.com/gateway.do?{data}".format(data=self.biz_content())
        return url
    

class WXPayProduct(Product):
    """ 微信支付的具体实现 """
        
    def operation(self) -> str:
        return "微信支付地址"


class BalanceProduct(Product):
    """ 余额支付 """
    
    def __init__(self, order: BaykeOrder) -> None:
        super().__init__(order)
        self.owner = order.owner
    
    def operation(self) -> str:
        return "余额支付"


def client(creator:Creator):
    return creator.some_operation()