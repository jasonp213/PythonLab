from __future__ import annotations

from datetime import datetime

from elasticsearch_dsl import Date, Document, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections


class Article(Document):
    title = Text(analyzer="snowball", fields={"raw": Keyword()})
    body = Text(analyzer="snowball")
    tags = Keyword()
    published_from = Date()
    lines = Integer()

    class Index:
        name = "blog"
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        self.lines = len(self.body.split())
        return super().save(**kwargs)

    def is_published(self):
        return datetime.now() >= self.published_from


if __name__ == "__main__":
    # Define a default Elasticsearch client
    connections.create_connection(hosts=["localhost"])

    # create the mappings in elasticsearch
    Article.init()

    # create and save and article
    article = Article(meta={"id": 43}, title="Hello world!", tags=["test"])
    article.body = """ looong text """
    article.published_from = datetime.now()
    article.save()

    article = Article.get(id=42)
    print(article.is_published())

    # Display cluster health
    print(connections.get_connection().cluster.health())
