import enum


class ContentType(enum.Enum):
    """枚举文章类型"""
    TEXT = 'text'  # 普通文章类型
    ALGORITHM_TEMPLATE = 'algorithm_template'  # 模板文章类型


class WXExceptions(enum.Enum):
    """微信公众平台设定的错误类型"""
    ACCESS_TOKEN_ERROR = {'error_code': 40014, 'msg': '不合法的 access_token ，请开发者认真比对 access_token 的有效性（如是'
                                                      '否过期），或查看是否正在为恰当的公众号调用接口'}
    ACCESS_TOKEN_EXPIRED = {'error_code': 40001, 'msg': '获取 access_token 时 AppSecret 错误，或者 access_token 无效。'
                                                        '请开发者认真比对 AppSecret 的正确性，或查看是否正在为恰当的公众'
                                                        '号调用接口'}