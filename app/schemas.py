from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime

    class Config:
        orm_mode: True

class CreateUser(BaseModel):
    email: EmailStr
    password: str