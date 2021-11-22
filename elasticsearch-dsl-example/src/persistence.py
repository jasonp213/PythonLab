from datetime import datetime
from elasticsearch_dsl import Document, InnerDoc, Integer, Text, Keyword, GeoPoint, Date


class Shakespeare(Document):
    """
    {
        "line_id": INT,
        "play_name": "String",
        "speech_number": INT,
        "line_number": "String",
        "speaker": "String",
        "text_entry": "String",
    }
    {
      "mappings": {
        "properties": {
            "speaker": {"type": "keyword"},
            "play_name": {"type": "keyword"},
            "line_id": {"type": "integer"},
            "speech_number": {"type": "integer"}
        }
      }
    }

    """
    line_id = Integer()
    play_name = Keyword()
    speech_number = Integer()
    line_number = Text()
    speaker = Keyword()
    text_entry = Text()


class Accounts(Document):
    """
    {
        "account_number": INT,
        "balance": INT,
        "firstname": "String",
        "lastname": "String",
        "age": INT,
        "gender": "M or F",
        "address": "String",
        "employer": "String",
        "email": "String",
        "city": "String",
        "state": "String"
    }
    """
    account_number = Integer()
    balance = Integer()
    firstname = Text()
    lastname = Text()
    age = Integer()
    gender = "M or F",
    address = Text()
    employer = Text()
    email = Text()
    city = Text()
    state = Text()

class LogStash(Document):
    """
    {
        "memory": INT,
        "geo.coordinates": "geo_point"
        "@timestamp": "date"
    }
    {
      "mappings": {
        "properties": {
          "geo": {
            "properties": {
              "coordinates": {
                "type": "geo_point"
              }
            }
          }
        }
      }
    }
    """
    memory = Integer()
    geo_coordinates = GeoPoint()
    timestamp = Date()
