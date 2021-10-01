from CjrInfo.server_settings import ES
from elasticsearch.helpers import bulk
from main_server.models.models import Content


def rebuild_es():
    docs = []
    contents = Content.objects.all()
    for content in contents:
        docs.append({
            '_index': 'content',
            '_source': {
                'media_id': content.media_id,
                'title': content.title,
                'tag': content.tag,
            }
        })
    bulk(client=ES, actions=docs)
    print(f'sync success')





