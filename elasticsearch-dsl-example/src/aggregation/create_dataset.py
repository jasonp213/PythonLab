import copy
import random
import time
from datetime import date

from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document, Keyword
from elasticsearch_dsl.connections import connections


def gen_data(times=300000):
    p1 = 'Joey'
    p2 = 'Tom'
    lookup = {
        0: p1,
        1: p2,
    }
    for _ in range(times):
        yield {
            '_index': 'tennis',
            'winner': lookup[random.randint(0, 1)]
        }


class TennisGameTemplate(Document):
    """
    PUT /_template/template_tennis
    {
      "settings": {"number_of_shards": 1},
      "aliases": {"Tennis": {}},
      "mappings": {"properties": {"winner": {"type": "keyword"}}},
      "index_patterns": ["tennis-*"],
      "version": 1
    }
    """
    winner = Keyword()

    # created_date = Date()

    class Index:
        name = 'tennis-*'
        aliases = {'tennis': {}}
        settings = {
            "number_of_shards": 1,
        }
        # the template of es-dsl-py `version` not working
        # src: https://github.com/elastic/elasticsearch-dsl-py/blob/58c02732658018333cfd5fa2f7b70d942773b0be/elasticsearch_dsl/index.py#L27
        # https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates-v1.html
        version = 1


def DocFactory():
    index_name = f"tennis-{date.today().strftime('%Y-%m-%d')}"

    new_cls = copy.copy(TennisGameTemplate)
    index_cls = getattr(new_cls, '_index')
    setattr(index_cls, '_name', index_name)

    return new_cls


connections.create_connection(hosts=['localhost'])

if __name__ == '__main__':
    connections.create_connection(hosts=['localhost'])

    TennisGame = DocFactory()

    print(f'_index._name: {TennisGame._index._name}, Index.name: {TennisGame.Index.name}')

    if not TennisGame._index.exists():
        print('')
        TennisGame.init()

    start = time.time()
    es = connections.get_connection()

    bulk(es, gen_data())

    print(f"setup done! spend: {time.time() - start}")
