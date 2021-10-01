from elasticsearch_dsl import connections, Q, Search

from CjrInfo.server_settings import ES


class EsSearch:
    """检索ES"""

    @classmethod
    def search_es_by_keyword(cls, keyword):
        """
        根据关键词检索ES
        :param keyword:
        :return: media_id list
        """
        res = []
        q = Q('match', title=keyword) | Q('match', tag=keyword) | Q('match', digest=keyword)
        response = Search(using=ES, index='content').query(q).execute()
        for hit in response:
            res.append(hit.media_id)
        return res




