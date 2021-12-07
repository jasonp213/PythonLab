import copy
import random
import time
from datetime import date

from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document, Keyword
from elasticsearch_dsl.connections import connections


def gen_data(times=10 * 1000 * 1000, player=200 * 1000, index='tennis'):
    times = max(times, player)
    # make sure each at least one
    for i in range(player):
        yield {
            '_index': index,
            'winner': f'player-{i}'
        }

    # such total to times
    for _ in range(times - player):
        yield {
            '_index': index,
            'winner': f'player-{random.randint(0, player)}'
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


if __name__ == '__main__':

    connections.create_connection(hosts=['localhost'])

    es = connections.get_connection()  # equal to es = elasticsearch.Elasticsearch()

    # the es-dsl-py no api the query template
    customer_templates = es.transport.perform_request("GET", "/_template/template-*")
    if 'template-tennis' not in customer_templates:
        print('create template')
        TennisGameTemplate._index.as_template('template-tennis').save()
    else:
        print('template exist')

    TennisGame = DocFactory()

    index_name = TennisGame._index._name

    print(f'_index._name: {index_name}, Index.name: {TennisGame.Index.name}')

    start = time.time()
    if not TennisGame._index.exists():
        print('Create index')
        TennisGame.init()

        es = connections.get_connection()

        bulk(es, gen_data(index=index_name))
    else:
        print('Index exist')

    print(f"setup done! spend: {time.time() - start}")
