from rest_framework import status

from collections import namedtuple


# 正常来说要有http_status这个属性的  但是因为主要调用微信公众平台的第三方服务器
# 如果http_status 不是200  第三方服务器就无法传递响应 所以其实所有报错的http_status最后都会变成200
# 但是这里还是要标明 真实的http status
CJR_Exceptions = namedtuple('CJR_Exceptions', 'inner_status msg http_status')


UNKNOWN_ERROR = CJR_Exceptions(10000, '服务器内部错误', status.HTTP_500_INTERNAL_SERVER_ERROR)


class SeverException(Exception):
    """
    全局异常基类
    """

    def __init__(self, exception=UNKNOWN_ERROR):
        super().__init__(exception)
        self.msg = exception.msg
        self.status = exception.inner_status
        self.http_status = exception.http_status


# ------------------------------------------------------------------------- #
#                              将使用的异常在此声明                           #
# ------------------------------------------------------------------------- #
WX_CRYPT_CHECK_FAIL = CJR_Exceptions(10001, '微信公众平台加密验证未通过', status.HTTP_403_FORBIDDEN)
WX_INTERFACE_FAIL = CJR_Exceptions(10002, '微信公众平台接口请求失败', status.HTTP_500_INTERNAL_SERVER_ERROR)

UNKNOWN_MATERIAL_TYPE = CJR_Exceptions(10003, '未知素材类型', status.HTTP_500_INTERNAL_SERVER_ERROR)
UNKNOWN_COMMAND = CJR_Exceptions(10004, '未知的命令', status.HTTP_404_NOT_FOUND)
NOT_RELEVANT_CONTENT = CJR_Exceptions(10005, '没有相关文章', status.HTTP_404_NOT_FOUND)






