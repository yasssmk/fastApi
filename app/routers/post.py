from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schema, oath2
from ..database import get_db, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

@router.get("/", response_model=List[schema.PostResponse])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM post ")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all()
    # # results = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all() 

    # post_with_votes = []

    # for post, vote_count in results:
    #     post_dict = post.__dict__
    #     post_dict['votes'] = vote_count
    #     post_with_votes.append(post_dict)

    return posts 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(post: schema.PostBase, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    # cursor.execute("INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = user_id.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schema.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    # cursor.execute("SELECT * FROM post WHERE id = %s", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    # cursor.execute("DELETE FROM post WHERE id = %s returning * ", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} was not found")
    
    if post.owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.PostResponse)
def update_post(id: str, post: schema.PostBase, db: Session = Depends(get_db), user_id: int = Depends(oath2.get_current_user)):
    # cursor.execute("UPDATE post SET title = %s, content= %s , published = %s WHERE id = %s returning * ", (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()
    print(user_id.id)
    print(post_to_update.owner_id)
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} was not found")
    
    if post_to_update.owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()