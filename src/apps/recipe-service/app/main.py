from typing import Union

from fastapi import FastAPI

from app.service.service import RecipeService

svc = RecipeService()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test_db():
    return svc.test()

@app.get("/greet/{name}")
def greet(name: str):
    return {"Greetings": name}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
