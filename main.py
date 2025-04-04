from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {
        "id": 1,
        "title": "Title of post 1",
        "content": "Content of post 1"
    },
    {
        "id": 2,
        "title": "Title of post 2",
        "content": "Content of post 2"
    },
    ]

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get('/posts')
async def get_posts():
    return {"data": my_posts}

@app.post('/posts')
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100)
    my_posts.append(post_dict)
    return {"message": "New post uploaded!", "data": post_dict}