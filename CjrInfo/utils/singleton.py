import logging
import traceback

from threading import Lock

logger = logging.getLogger('log')


class Singleton:
    __instance = None
    __lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__lock.acquire()
        try:
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
        except Exception as e:
            # TODO 后续此处错误应添加到日志中
            traceback.format_exc()
            logger.error(e)
            pass
        finally:
            if cls.__lock.locked():
                cls.__lock.release()
        return cls.__instance


class CallInstance(type):
    """
    直接调用实例
    """
    def __call__(cls, *args, **kwargs):
        cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance()





