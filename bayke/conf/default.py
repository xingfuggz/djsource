import datetime


DEFAULTS_CONF = {
    
    # 站点URL，最后不带斜杠
    "SITE_URL": "http://127.0.0.1:3000",
    
    "SITE_HEADER": "Bayke",
    "SITE_TITLE": "Bayke",
    
    "ADMIN_MENUS": True,
    
    "ADMIN_MENUS_DATAS": None,
    
    "HAS_MESSAGE_EAMIL": False,
    
    "HAS_SEARCH_CATEGORY": False,
    
    "PC_LOGO": "baykeshop",
    
    # 首页楼层数量及分类显示数量
    "HOME_NAV_COUNT": 5,
    
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
    
    # 支付宝支付相关配置
    "ALIPAY_APPID": "2021000122666025",
    "ALIPAY_NOTIFY_URL": "bayke:alipay-success",
    "ALIPAY_RETURN_URL": "bayke:alipay-success",
    "ALIPAY_PRIVATE_KEY":"bayke/payment/alipay/keys/app_private_key.pem",
    "ALIPAY_PUBLIC_KEY": "bayke/payment/alipay/keys/alipay_public_key.pem",
    "ALIPAY_SIGN_TYPE": "RSA2",  # RSA 或者 RSA2
}
