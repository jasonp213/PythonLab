"""
Here define the Elasticsearch(kibana) document

https://www.elastic.co/guide/en/kibana/7.6/tutorial-build-dashboard.html#load-dataset

"""

from elasticsearch_dsl import Document, Integer, Text, Keyword, GeoPoint, Date


class Shakespeare(Document):

    line_id = Integer()
    play_name = Keyword()
    speech_number = Integer()
    line_number = Text()
    speaker = Keyword()
    text_entry = Text()


class Accounts(Document):

    account_number = Integer()
    balance = Integer()
    firstname = Text()
    lastname = Text()
    age = Integer()
    gender = Keyword()  # "M or F"
    address = Text()
    employer = Text()
    email = Text()
    city = Text()
    state = Text()

    class Index:
        name = 'bank'

        settings = {
            "number_of_shards": 1,
            # Note that the number of replicas 0 means
            "number_of_replicas": 0
        }


class LogStash(Document):

    memory = Integer()
    geo_coordinates = GeoPoint()
    timestamp = Date()

    class Index:
        """
        this define the index meta
        """
        name = 'logstash'
