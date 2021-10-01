import hashlib
import json
import logging
from typing import List

import requests

from django.core.cache import cache
from django.db import transaction
from elasticsearch.helpers import bulk

from CjrInfo.server_settings import TOKEN, APP_ID, APP_SECRET, ES
from main_server.enums import WXExceptions
from main_server.models.models import Content, Media
from utils import exceptions, time_utils

logger = logging.getLogger('log')


class ManageAccessToken:
    """管理调用微信接口所需要的AccessToken"""

    @staticmethod
    def get_token_from_wx():
        token_url = f'https://api.weixin.qq.com/cgi-bin/token?' \
                    f'grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}'
        try:
            response = requests.get(token_url)
        except Exception as e:
            logger.info(f'access token 获取失败 {e}')
            raise e
        return json.loads(response.text)

    @staticmethod
    def set_token_to_cache(token, expire=2 * 60 * 60):
        try:
            cache.set("wx_access_token", token, timeout=expire)
        except Exception as e:
            logger.info(f'wx token 缓存设置失败: {e}')

    @classmethod
    def get_token(cls):
        if cache.has_key('wx_access_token') and cache.ttl("wx_access_token"):
            return cache.get('wx_access_token')


class WXServer(ManageAccessToken):
    """微信接口相关服务"""
    retry_count = 0

    def __call__(self, *args, **kwargs):
        return self

    @staticmethod
    def check_command_source(echostr, timestamp, nonce, signature):
        """
        在微信公众平台配置自定义接口时候需要进行验证
        :param echostr: 验证通过返回该字段
        :param timestamp:
        :param nonce:
        :param signature:
        :return:
        """
        tmp = [TOKEN, timestamp, nonce]
        tmp.sort()
        cryptographic = hashlib.sha1(''.join(tmp).encode('utf-8')).hexdigest()
        if cryptographic == signature:
            return echostr
        raise exceptions.SeverException(exceptions.WX_CRYPT_CHECK_FAIL)

    def request_to_wx(self, url, headers, **kwargs):
        """
        使用它向WX发起一个请求 可以帮助你处理请求失败的逻辑
        :param headers:
        :param url:
        :return:
        """
        logger.info(f'本次请求：{url}\n{headers}')
        try:
            response = requests.post(url, data=headers, json={'Content_Type': 'application/json'}, **kwargs)
            response.encoding = 'utf-8'
        except Exception as e:
            logger.error(f'素材管理请求出错 {e}')
            raise exceptions.SeverException(exceptions.WX_INTERFACE_FAIL)
        response_data = response.json()
        errcode = response_data.get('errcode')
        # 如果是因为token失效错误，则有三次重试
        if errcode == WXExceptions.ACCESS_TOKEN_EXPIRED.value.get('error_code') and self.retry_count < 3:
            response = self.get_token_from_wx()
            response.encoding = 'utf-8'
            self.set_token_to_cache(response['access_token'], expire=response['expires_in'] - 60 * 10)
            self.retry_count += 1
            return self.request_to_wx(url, headers, **kwargs)
        if errcode:
            logger.error(f'微信接口请求错误：{response_data}')
            raise exceptions.SeverException(exceptions.WX_INTERFACE_FAIL)
        return response_data


class ManageMaterial(ManageAccessToken):
    """素材管理相关接口"""
    time_util = time_utils.TimeUtils()
    retry_cnt = 0
    wx_handler = WXServer()

    def get_offset_from_wx(self, material_type='news', offset=0, count=20) -> dict:
        """
        获取部分指定类型的素材
        :param material_type: 获取的素材类型
        :param offset: 从该位置开始获取
        :param count: 本次获取的数量
        :return:
        """
        material_url = f'https://api.weixin.qq.com/cgi-bin/material/batchget_material?' \
                       f'access_token={self.get_token()}'
        headers = json.dumps({
            'type': material_type,
            'offset': offset,
            'count': count
        })
        wx_handler = WXServer()
        return self.wx_handler.request_to_wx(material_url, headers)

    def get_all_material_from_wx(self, material_type='news') -> List:
        """
        获取指定类型的全部素材
        :return:
        """
        response_json = self.get_offset_from_wx(material_type=material_type)
        items = response_json['item']
        total_count = response_json['total_count']
        item_count = response_json['item_count']
        for i in range(item_count, total_count, 20):
            response_json = self.get_offset_from_wx(material_type=material_type, offset=i)
            items.extend(response_json['item'])
        return items

    def get_single_material_from_wx(self, media_id):
        """
        根据media_id获取一个资源
        :param media_id:
        :return: 返回微信响应的response
        """
        material_url = f'https://api.weixin.qq.com/cgi-bin/material/get_material?' \
                       f'access_token={self.get_token()}'
        headers = json.dumps({
            "media_id": media_id
        })
        return self.wx_handler.request_to_wx(material_url, headers)

    @transaction.atomic
    def sync_media(self):
        """
        同步media素材到数据库
        :return:
        """
        items = []
        res = self.get_all_material_from_wx(material_type='image')
        for images in res:
            items.append(Media(
                media_id=images['media_id'],
                name=images['name'],
                url=images['url'],
                create_time=self.time_util.timestamp_to_time(images['update_time']),
                update_time=self.time_util.timestamp_to_time(images['update_time']),
            ))
        if items:
            Media.objects.bulk_create(items)

    @transaction.atomic
    def sync_content(self):
        """
        同步文本素材到数据库和ES
        :return:
        """
        res = self.get_all_material_from_wx()
        items, es_items = [], []
        for contents in res:
            media_id = contents['media_id']
            content = contents['content']
            create_time = content['create_time']
            update_time = content['update_time']
            for news_item in content['news_item']:
                logger.info(f'导入new_item成功: {news_item["title"]}')
                items.append(Content(
                    media_id=media_id,
                    content=news_item['content'],
                    author=news_item['author'],
                    title=news_item['title'],
                    show_cover_pic=news_item['show_cover_pic'],
                    thumb_media_id=news_item['thumb_media_id'],
                    thumb_media_url=news_item['thumb_media_url'],
                    digest=news_item['digest'],
                    content_url=news_item['url'],
                    source_url=news_item['content_source_url'],
                    create_time=self.time_util.timestamp_to_time(create_time),
                    update_time=self.time_util.timestamp_to_time(update_time),
                ))
                es_items.append({
                    '_index': 'content',
                    '_source': {
                        'title': news_item['title'],
                        'tag': news_item.get('tag'),
                        'digest': news_item['digest'],
                    }
                })
        if items:
            Content.objects.bulk_create(items)
        if es_items:
            bulk(ES, actions=es_items)

    @transaction.atomic
    def update_content(self):
        """
        更新一个字段
        :return:
        """
        res = self.get_all_material_from_wx()
        for contents in res:
            content = contents['content']
            for news_item in content['news_item']:
                Content.objects.filter(title=news_item['title']).update(thumb_media_url=news_item['thumb_url'])
        logger.info('sync success')

