from fastapi import FastAPI
from app.routers import auth, posts
from app.database import engine, Base

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include routers for authentication and posts endpoints
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
