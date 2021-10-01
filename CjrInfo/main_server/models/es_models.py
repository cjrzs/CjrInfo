from elasticsearch_dsl import DocType, Text


class ContentEsModel(DocType):
    media = Text()
    title = Text()
    tag = Text()
    digest = Text()

    class Meta:
        index = 'content'





