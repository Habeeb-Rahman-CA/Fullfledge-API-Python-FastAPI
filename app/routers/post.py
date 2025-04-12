from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
    dependencies=[Depends(oauth2.get_current_user)]
    )

# Get All Posts
@router.get('/')
async def get_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts

# Get Post By Id
@router.get('/{id}')
async def get_post(id: str, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post

# Create Post
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.CreatePost, db:Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Delete Post By Id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:str, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post By Id
@router.put('/{id}')
async def update_post(id: str, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    edit_post = post_query.first()
    if edit_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} doesn't exist!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())
    return post_query.first()
