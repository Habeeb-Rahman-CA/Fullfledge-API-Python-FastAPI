from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

# http://127.0.0.1:8000/docs#/ Open Swagger Docs

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

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get('/posts')
async def get_posts():
    return {"data": my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100)
    my_posts.append(post_dict)
    return {"message": "New post uploaded!", "data": post_dict}

@app.get('/posts/latest')
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"message": "Loaded latest post", "detail": post}

@app.get('/posts/{id}')
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")
    return {"message": f"Here is post {id}!", "data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": f"Post {id} updated!", "data": post_dict}