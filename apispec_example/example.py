#!/usr/bin/env python3
"""
this example
modify base on https://github.com/marshmallow-code/apispec
only implement a little detail with https://docs.thecatapi.com/

"""
from dataclasses import dataclass
from urllib import request
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, redirect, url_for
from marshmallow import Schema, fields
import requests


# Create an APISpec
spec = APISpec(
    title="Swagger Petstore",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


# Define the data struct
@dataclass
class Category:
    id: int
    name: str


@dataclass
class Pet:
    category: list
    id: str
    url: str
    width: int
    height: int


# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)


class PetSchema(Schema):
    category = fields.List(fields.Nested(CategorySchema))
    id = fields.Str()
    url = fields.Str()
    width = fields.Int()
    height = fields.Int()


# Optional security scheme support
api_key_scheme = {"type": "apiKey", "in": "header", "name": "X-API-Key"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)


# Optional Flask support
app = Flask(__name__)


def get_random_pet():
    ret = requests.get("https://api.thecatapi.com/v1/images/search")
    data = ret.json()[0]

    del data["breeds"]
    cat = Category(id=1, name="cat")
    p = Pet(**data, category=[cat])
    return p


@app.route("/")
def index():
    return redirect(url_for("random_spec"))


@app.route("/random")
def random_pet():
    """A cute furry animal endpoint.
    ---
    get:
      description: Get a random pet
      security:
        - ApiKeyAuth: []
      responses:
        200:
          content:
            application/json:
                schema: PetSchema
    """
    pet = get_random_pet()
    return PetSchema().dump(pet)


@app.route("/random/spec")
def random_spec():
    """Here commen
    ---
    get:
      description: Get swagger
      responses:
        200:
          content:
            application/json:
    """
    import json

    return json.dumps(spec.to_dict(), indent=2)


# Register the path and the entities within it
with app.test_request_context():
    spec.path(view=random_pet)
    spec.path(view=random_spec)
