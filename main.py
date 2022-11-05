from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    first_name: str
    last_name: str



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/post")
async def post():
    return {"message": "This is post"}


@app.post("/create")
def create(data: dict = Body(...)):
    print(data)
    return {"new_post": f"name: {data['name']} last_name: {data['last_name']}"}


@app.post("/create_post")
def create_post(new_post:Post):
    print(new_post)
    print(new_post.first_name)
    print(new_post.last_name)
    return {"user":"new_post"}