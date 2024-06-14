from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    SQLAlchemy model for the users table.

    Attributes:
    - id (int): Primary key.
    - email (str): Unique email of the user.
    - hashed_password (str): Hashed password of the user.
    - posts (relationship): Relationship to the Post model.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    """
    SQLAlchemy model for the posts table.

    Attributes:
    - id (int): Primary key.
    - text (str): Content of the post.
    - owner_id (int): Foreign key to the users table.
    - owner (relationship): Relationship to the User model.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
