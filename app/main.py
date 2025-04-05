from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# http://127.0.0.1:8000/docs#/ Open Swagger Docs

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi_app', user='postgres', password='habizz', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Failed to connect the database.")
        print("Error: ", error)
        time.sleep(2)

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

# Get All Post
@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message":"Retrieving all posts."," data": posts}

# Get Post By Id
@app.get('/posts/{id}')
async def get_post(id: str):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found!")
    return {"message": f"Here is post {id}!", "data": post}

# Create Post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": "New post uploaded!", "data": new_post}

# Delete Post By Id
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:str):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post By Id
@app.put('/posts/{id}')
async def update_post(id: str, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    return {"message": f"Post {id} updated!", "data": updated_post}