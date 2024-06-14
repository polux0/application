from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base schema for User model with email field.
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user with password field.
    """
    password: str


class User(UserBase):
    """
    Schema for representing a user with id field.
    """
    id: int

    class Config:
        from_attributes = True  # In order to enable attribute extraction from ORM model


class PostBase(BaseModel):
    """
    Base schema for Post model with text field.
    """
    text: str


class PostCreate(PostBase):
    """
    Schema for creating a new post.
    """
    pass


class Post(PostBase):
    """
    Schema for representing a post with id and owner_id fields.
    """
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # In order to enable attribute extraction from ORM model
