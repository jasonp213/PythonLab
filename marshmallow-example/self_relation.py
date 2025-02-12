from __future__ import annotations

from dataclasses import dataclass

import marshmallow
from marshmallow import Schema, fields, post_load


@dataclass
class TagDto:
    id: int
    name: str
    parent: dict = None


class NestedTag(Schema):
    id = fields.Integer()
    name = fields.String()
    parent = fields.Nested("self", default=None)

    @post_load
    def create_dto(self, data, many=False, partial=False):
        return TagDto(**data)


tag_a = {"id": 1, "name": "book"}
tag_b = {"id": 2, "name": "novel", "parent": tag_a}
tag_c = {"id": 3, "name": "draw", "parent": 1}

if __name__ == "__main__":
    schema = NestedTag()
    a = schema.load(tag_a)
    print(f"{a=}")
    b = schema.load(tag_b)
    print(f"{b=}")
    try:
        c = schema.load(tag_c)
    except marshmallow.ValidationError as err:
        print(f"{err=}")
