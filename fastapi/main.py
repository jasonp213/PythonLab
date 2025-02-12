from __future__ import annotations

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    ret = {"message": "Hello World"}
    return ret


@app.get("/item")
async def item(q):
    return q


@app.get("/items")
async def items(*args):
    return args
