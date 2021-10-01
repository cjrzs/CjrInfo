import logging

from django.http import HttpResponse
from utils import time_utils, exceptions, singleton

logger = logging.getLogger('log')


class CjrResponse(singleton.Singleton, metaclass=singleton.CallInstance):
    """被动响应消息
    以下注释代码用于正确性调试  勿删
    time_util = time_utils.TimeUtils()
    res = f'''
    <xml>
    <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
    <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
    <CreateTime>{int(time_util.get_now_timestamp())}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    </xml>
    '''
    """
    def __init__(self, content, **kwargs):
        self.kwargs = kwargs
        self.to_user_name = content.get('to_user_name')
        self.from_user_name = content.get('from_user_name')
        self.msg_content_type = content.get('msg_content_type')
        self.response_content = content.get('response_content')

        time_util = time_utils.TimeUtils()
        self.now_timestamp = int(time_util.get_now_timestamp())

    def __call__(self, *args, **kwargs):
        return self.resolver_match()

    def resolver_match(self):
        """
        根据消息类型解析消息，目前支持两种消息类型
        text 文本类型   news 图文类型
        当消息类型是文本时候msg_content_type字段是str 当消息类型是news的时候该字段是dict

        if msg_content_type == text:
            response_content是文本消息
        elif msg_content_type == news:
            response_content = {
                title: '文章标题',
                content: '文章内容',
                pic_url: '图片URL',
                url: '点击图文跳转的链接'
            }

        :return:
        """
        if self.msg_content_type == 'text':
            msg = f"""
<xml>
<ToUserName><![CDATA[{self.to_user_name}]]></ToUserName>
<FromUserName><![CDATA[{self.from_user_name}]]></FromUserName>
<CreateTime>{self.now_timestamp}</CreateTime>
<MsgType><![CDATA[{self.msg_content_type}]]></MsgType>
<Content><![CDATA[{self.response_content}]]></Content>
</xml>
"""
        elif self.msg_content_type == 'news':
            msg = f"""
<xml>
<ToUserName><![CDATA[{self.to_user_name}]]></ToUserName>
<FromUserName><![CDATA[{self.from_user_name}]]></FromUserName>
<CreateTime>{self.now_timestamp}</CreateTime>
<MsgType><![CDATA[{self.msg_content_type}]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[{self.response_content['title']}]]></Title>
<Description><![CDATA[{self.response_content['description']}]]> </Description>
<PicUrl><![CDATA[{self.response_content['pic_url']}]]></PicUrl>
<Url><![CDATA[{self.response_content['url']}]]></Url>
</item>
</Articles>
</xml>
"""

        else:
            raise exceptions.SeverException(exceptions.UNKNOWN_ERROR)
        logger.debug(f'最终响应: {msg}')
        return HttpResponse(msg, content_type='text/xml', **self.kwargs)

