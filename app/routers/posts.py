from app.models import Post
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, get_current_user
from cachetools import TTLCache

router = APIRouter()
cache = TTLCache(maxsize=100, ttl=300)


@router.post("/addpost", response_model=schemas.Post)
def add_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Endpoint to add a new post.

    Args:
    - post (PostCreate): PostCreate schema object.
    - db (Session): Database session.
    - current_user (User): Current authenticated user.

    Returns:
    - Post: Created Post object.
    """
    return crud.create_post(db=db, post=post, user_id=current_user.id)


@router.get("/getposts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Endpoint to get all posts by the current authenticated user.

    Args:
    - db (Session): Database session.
    - current_user (User): Current authenticated user.

    Returns:
    - list[Post]: List of Post objects.
    """
    user_id = current_user.id
    if user_id in cache:
        return cache[user_id]
    posts = crud.get_posts_by_user(db, user_id=user_id)
    cache[user_id] = posts
    return posts


@router.delete("/deletepost/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Endpoint to delete a post by its ID.

    Args:
    - post_id (int): ID of the post to delete.
    - db (Session): Database session.
    - current_user (User): Current authenticated user.

    Returns:
    - dict: Confirmation message.

    Raises:
    - HTTPException: If the post is not found.
    """
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == current_user.id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    crud.delete_post(db=db, post_id=post_id)
    return {"msg": "Post deleted successfully"}
