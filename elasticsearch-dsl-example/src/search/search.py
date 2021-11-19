from elasticsearch import Elasticsearch

client = Elasticsearch()

def search():
    response = client.search(
        index='my-index',
        body={
            'query': {
                'filtered': {
                    'query': {
                        'bool': {
                            'must': [{'match': {'title':'python'}}],
                            'must_not': [{'match': {'description':'beta'}}],
                        }

                    },
                    'filter': {'term': {'category': 'search'}}
                }
            },
            'args': {
                'per_tag'
            }
        }
    )