from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.get('/posts')
async def get_posts():
    return {"data": "This is your posts"}

@app.post('/posts')
async def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": "Successfully created post!"}