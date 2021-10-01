from django.db import models
from utils.time_utils import TimeUtils


class BaseModel(models.Model):
    """model基类 系统中所有model都应继承该类"""
    now = TimeUtils.get_now_time()
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)
    delete_time = models.DateTimeField(default=now, null=True)

    class Meta:
        abstract = True





