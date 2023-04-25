import datetime
from django.conf import settings


DEFAULTS_CONF = {
    
    # 手机号验证正则
    "REGEX_PHONE": "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$",
    # 邮箱验证正则
    "REGEX_EMAIL": "^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
    
    # 邮箱验证码过期时间
    "EMAIL_CODE_EXP": datetime.timedelta(seconds=300),
    # 验证码随机范围
    "CODE_CHAR": "1234567890",
    # 验证码长度
    "CODE_LENGTH": 4,
    
    "ALIPAY_APPID": "2021000116697536",
    "ALIPAY_NOTIFY_URL": "baykeshop:alipay_notify",
    "ALIPAY_RETURN_URL": "baykeshop:alipay_notify",
    "ALIPAY_PRIVATE_KEY":"bayke/payment/alipay/keys/app_private_key.pem",
    "ALIPAY_PUBLIC_KEY": "bayke/payment/alipay/keys/app_public_key.pem",
    "ALIPAY_SIGN_TYPE": "RSA2",  # RSA 或者 RSA2
    "ALIPAY_DEBUG": settings.DEBUG,
}
