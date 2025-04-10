from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user

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

app.include_router(post.router)
app.include_router(user.router)