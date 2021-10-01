"""
命令处理逻辑（所有命令均以指定前缀开始）：
    /z: 触发模糊检索。此时会将所有的与关键词相关的内容全部编号并且返回。
    /c: 触发指定检索。此时会检测命令格式：
            1、如果命令可以转换成int型，则认为是编号，返回编号对应的文章。
            2、如果无法转换成编号。则返回与命令相似度最高的一篇文章。
            3、默认触发的命令是“c”。
"""
import logging

from CjrInfo.server_settings import COMMAND_MAP
from utils.exceptions import SeverException, UNKNOWN_COMMAND, NOT_RELEVANT_CONTENT
from main_server.servers import db_server, es_server

logger = logging.getLogger('log')


class CommandHandler:

    def __init__(self, message: str):
        """
        初始化命令
        :param message:
        """
        for ch in ['/', '!', '！', '。', '-', '~']:
            if message[0] == ch:
                message = '/' + message[1:]
                break
        if message[0] == '/':
            for item in COMMAND_MAP.keys():
                if message.startswith(item):
                    self.command = item
                    self.message = message[len(item):].strip()
                    break
            else:
                raise SeverException(UNKNOWN_COMMAND)
        else:
            self.command = '/c'
            self.message = message.strip()
        logger.debug(f'接收到的消息: {self.message}')
        logger.debug(f'接收到的命令: {self.command}')

    def __call__(self, *args, **kwargs):
        return self.process_message()

    def process_message(self):
        """
        处理命令，并且返回对应处理器
        :return:
        """
        handler = getattr(self, COMMAND_MAP[self.command])
        return handler()

    def fuzzy_search(self):
        """
        命令：/z 触发模糊检索
        :return: 1 title1
                 2 title2
                 3 title3
        """
        media_ids = es_server.EsSearch.search_es_by_keyword(self.message)
        db_handler = db_server.DbHandler('content')
        materials = db_handler.get_data_by_media_id(media_ids)
        return '\n'.join([f'<{str(item.id)}>  {item.title}' for item in materials])

    def single_search(self):
        """
        默认命令：/c 触发指定检索
        :return:
        """
        db_handler = db_server.DbHandler('content')
        if self.message.isdigit():
            material = db_handler.get_data_by_id(int(self.message)).first()
            if not material:
                raise SeverException(NOT_RELEVANT_CONTENT)
        else:
            media_ids = es_server.EsSearch.search_es_by_keyword(self.message)
            if not media_ids:
                raise SeverException(NOT_RELEVANT_CONTENT)
            material = db_handler.get_data_by_media_id([media_ids[0]]).first()
        res = {
            'title': material.title,
            'description': material.digest,
            'pic_url': material.thumb_media_url,
            'url': material.content_url,
        }
        return res


