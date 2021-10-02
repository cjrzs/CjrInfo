import xmltodict

from django.http import HttpResponse
from rest_framework.views import APIView

from main_server.servers import wx_server, command_server
from utils.sync_db_to_es import rebuild_es
from utils.server_response import CjrResponse


class ReceiveWeChatMsgView(APIView):
    """接收微信消息"""
    # TODO 请求整体流程待封装

    @staticmethod
    def get(request):
        signature = request.GET.get('signature')
        echostr = request.GET.get('echostr')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        wechat = wx_server.WXServer()
        res = wechat.check_command_source(echostr, timestamp, nonce, signature)
        return HttpResponse(res)

    @staticmethod
    def post(request):
        xml_data = xmltodict.parse(request.body)
        data = xml_data.get('xml')
        to_user_name = data.get('ToUserName')
        from_user_name = data.get('FromUserName')
        receive_msg = data.get('Content')
        # TODO 重复请求待补充 日志待收集
        msg_id = data.get('MsgId')
        message_type = data.get('MsgType')
        event = data.get('Event')
        res = {
            'to_user_name': from_user_name,
            'from_user_name': to_user_name,
        }
        if message_type == 'event':
            res.update({
                'msg_content_type': 'text',
                'response_content': '你好，欢迎你关注我，由于微信官方接口更新，暂时获取不了新的图文消息，因此希望您能先看一下'
                                    '写给你的一封信。https://mp.weixin.qq.com/s/FNVnAVa3NQZNuZGHEbMV9g'
            })
        else:
            content = command_server.CommandHandler(receive_msg).process_message()
            if not content:
                content = '没有相关文章'
            res.update({
                'msg_content_type': 'text',
                'response_content': content
            })
            if isinstance(content, dict):
                res['msg_content_type'] = 'news'
        return CjrResponse(res)


class SyncMaterialToDatabase(APIView):
    """同步指定类型全部素材到数据库"""

    def post(self, request):
        material_type = request.data.get('material_type')
        material_handler = wx_server.ManageMaterial()
        if material_type == 'image':
            material_handler.sync_media()
        elif material_type == 'content':
            material_handler.sync_content()
        return HttpResponse('sync success')


class EsRebuild(APIView):
    """重建ES中的数据"""

    def post(self, request):
        rebuild_es()
        return HttpResponse('sync success')






