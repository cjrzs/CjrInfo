from django.db import models

from main_server.models.base_models import BaseModel
from main_server.enums import ContentType


class Media(BaseModel):
    """其他素材模型（图片、语音、视频等）"""
    media_id = models.CharField(max_length=200, db_index=True)
    name = models.CharField(max_length=200, null=True, default='未命名素材')
    url = models.CharField(max_length=200)


class Content(BaseModel):
    """文章素材模型"""
    media_id = models.CharField(max_length=200, db_index=True)
    ContentType_CHOICES = [
        (ContentType.ALGORITHM_TEMPLATE.value, ContentType.ALGORITHM_TEMPLATE.value),
        (ContentType.TEXT.value, ContentType.TEXT.value)
    ]
    content_type = models.CharField(max_length=200, choices=ContentType_CHOICES, default=ContentType.TEXT.value)
    tag = models.CharField(max_length=200, null=True)  # 标签 用于ES检索
    author = models.CharField(max_length=200, default='一只猫咪不加糖')
    title = models.CharField(max_length=500, null=True)
    show_cover_pic = models.BooleanField(default=True)  # 是否显示封面
    thumb_media_id = models.CharField(max_length=200, null=True)  # 封面图片
    thumb_media_url = models.CharField(max_length=200, null=True)
    digest = models.CharField(max_length=2000, null=True)  # 摘要
    content_url = models.CharField(max_length=200, null=True)  # 本文的URL
    source_url = models.CharField(max_length=200, null=True)  # 原文的URL（阅读原文）



