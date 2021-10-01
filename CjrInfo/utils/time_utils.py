import pytz

from django.utils import timezone
from utils.singleton import Singleton


class TimeUtils(Singleton):
    """
    为统一系统中的时间表示，使用时间戳的请使用本文件内方法。
    """

    def __init__(self, timezone='UTC'):
        self.timezone = timezone

    @classmethod
    def get_now_time(cls):
        """
        获取当前时间 示例：2021-09-28 10:50:02.674351+00:00 (UTC时间)
        :return:
        """
        return timezone.now()

    def timestamp_to_time(self, timestamp: str):
        """
        时间戳转时间 示例：2021-09-16 17:24:42
        :param timestamp:
        :return:
        """
        tz = pytz.timezone(self.timezone)
        dt = pytz.datetime.datetime.fromtimestamp(float(timestamp), tz)
        return dt

    def get_now_timestamp(self):
        """
        获取当前时间的时间戳 示例：1632893693
        :return:
        """
        return int(self.get_now_time().timestamp())





