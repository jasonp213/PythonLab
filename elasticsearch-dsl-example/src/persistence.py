"""
Here define the Elasticsearch(kibana) document

https://www.elastic.co/guide/en/kibana/7.6/tutorial-build-dashboard.html#load-dataset

"""

from elasticsearch_dsl import Document, Integer, Text, Keyword, GeoPoint, Date
from elasticsearch_dsl.connections import connections


class Shakespeare(Document):
    line_id = Integer()
    play_name = Keyword()
    speech_number = Integer()
    line_number = Text()
    speaker = Keyword()
    text_entry = Text()


class Bank(Document):
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
        name = "bank"

        settings = {"number_of_shards": 1, "number_of_replicas": 0}


class LogStash(Document):
    memory = Integer()
    geo_coordinates = GeoPoint()
    timestamp = Date()

    class Index:
        """
        this define the index meta
        """

        name = "logstash-*"
        aliases = {
            "logstash": {
                # here could put filter
            }
        }


def setup_log():
    alias = "logstash"
    patten = "logstash-*"  # using wildcard char

    template = LogStash._index.as_template(alias, patten)

    return template.save()


if __name__ == "__main__":
    # python shell template script
    # import os
    #
    # sys.path.append(f'{os.getcwd()}/elasticsearch-dsl-example/src')
    # from persistence import *
    # from
    # from elasticsearch_dsl.connections import connections

    connections.create_connection(hosts=["localhost"])

    print(setup_log())
