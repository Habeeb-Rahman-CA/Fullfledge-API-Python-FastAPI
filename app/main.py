from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get('/')
async def root():
    return {"message": "Hello World"}

# Get All Posts
@app.get('/posts')
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"message":"Retrieving all posts."," data": posts}

# Get Post By Id
@app.get('/posts/{id}')
async def get_post(id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"message": f"Here is post {id}!", "data": post}

# Create Post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.Post, db:Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "New post uploaded!", "data": new_post}

# Delete Post By Id
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post By Id
@app.put('/posts/{id}')
async def update_post(id: str, post: schemas.Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    edit_post = post_query.first()
    if edit_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(edit_post)
    return {"message": f"Post {id} updated!", "data": edit_post}