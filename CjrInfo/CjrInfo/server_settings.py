import os

from elasticsearch import Elasticsearch

# 公众号配置
TOKEN = os.getenv('TOKEN')
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')

# ES服务器地址
ES_IP = os.getenv('ES_IP')
ES = Elasticsearch(f'http://{ES_IP}:9200/')

# 命令配置
COMMAND_MAP = {
    '/z': 'fuzzy_search',
    '/c': 'single_search',
}



