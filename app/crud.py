from sqlalchemy.orm import Session
from app.models import User, Post
from app.schemas import UserCreate, PostCreate


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email from the database.

    Args:
    - db (Session): Database session.
    - email (str): User email.

    Returns:
    - User: User object if found, None otherwise.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
    - db (Session): Database session.
    - user (UserCreate): UserCreate schema object.

    Returns:
    - User: Created User object.
    """
    # TODO: Replace placeholder `fake_hashed_password` with proper password hashing ( for example: passlib )
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_post(db: Session, post: PostCreate, user_id: int):
    """
    Create a new post in the database.

    Args:
    - db (Session): Database session.
    - post (PostCreate): PostCreate schema object.
    - user_id (int): ID of the post owner.

    Returns:
    - Post: Created Post object.
    """
    db_post = Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts_by_user(db: Session, user_id: int):
    """
    Retrieve all posts by a specific user from the database.

    Args:
    - db (Session): Database session.
    - user_id (int): ID of the user.

    Returns:
    - list[Post]: List of Post objects.
    """
    return db.query(Post).filter(Post.owner_id == user_id).all()


def delete_post(db: Session, post_id: int):
    """
    Delete a post from the database by its ID.

    Args:
    - db (Session): Database session.
    - post_id (int): ID of the post to be deleted.
    """
    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()
