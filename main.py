from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get('/posts')
async def get_posts():
    return {"data": "This is your posts"}

@app.post('/posts')
async def create_post(new_post: Post):
    print(new_post.model_dump())
    return {"message": "New post uploaded!"}