from typing import List

from main_server.models import models
from utils.exceptions import SeverException, UNKNOWN_MATERIAL_TYPE
from utils.singleton import Singleton


class DbHandler(Singleton):
    """管理向DB发起的请求"""

    def __init__(self, material_type):
        self.material_type = material_type
        if self.material_type == 'content':
            self.model = models.Content
        elif self.material_type == 'media':
            self.model = models.Media
        else:
            raise SeverException(UNKNOWN_MATERIAL_TYPE)

    def get_data_by_media_id(self, media_ids: List):
        """
        通过media_id获取数据
        :param media_ids: List
        :return:
        """
        materials = self.model.objects.filter(media_id__in=media_ids)
        return materials

    def get_data_by_id(self, id: int):
        """
        通过自增ID获取数据
        :param id:
        :return:
        """
        materials = self.model.objects.filter(id=id)
        return materials








