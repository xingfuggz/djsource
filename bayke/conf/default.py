import datetime

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
}
