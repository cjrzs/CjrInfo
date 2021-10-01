import traceback

import xmltodict
from django.http import HttpResponse, RawPostDataException
from utils.exceptions import SeverException, UNKNOWN_ERROR

from utils.server_response import CjrResponse


class ExceptionMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exception(request, exception):
        # TODO 封装完请求接收流程之后 这里要改掉
        try:
            xml_data = xmltodict.parse(request.body)
        except RawPostDataException as e:
            print(traceback.format_exc())
            return HttpResponse(e)
        data = xml_data.get('xml')
        to_user_name = data.get('ToUserName')
        from_user_name = data.get('FromUserName')
        msg = UNKNOWN_ERROR.msg
        if isinstance(exception, SeverException):
            msg = exception.msg
        res = {
            'to_user_name': from_user_name,
            'from_user_name': to_user_name,
            'msg_content_type': 'text',
            'response_content': msg,
        }
        print(traceback.format_exc())
        # TODO 后续完善日志系统之后，将错误的request_id记录在日志中。

        return CjrResponse(res, status=200)



