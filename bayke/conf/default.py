import datetime

DEFAULTS_CONF = {
    
    "CODE_CHAR": "1234567890",
    "CODE_LENGTH": 4,

    "REGEX_PHONE": "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$",
    "REGEX_EMAIL": "^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
    
    # 邮箱验证码过期时间
    "EMAIL_CODE_EXP": datetime.timedelta(seconds=300)
}
