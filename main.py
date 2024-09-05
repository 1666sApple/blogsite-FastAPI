from fastapi import FastAPI
from routers import article, blog_get, blog_post, user
from db import models
from db.database import engine

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)

@app.get(
    '/',
    summary="Home Endpoint", 
    description="Returns a welcome message.",
    response_description="A JSON object containing a welcome message."
)
def home():
    """
    Home endpoint that returns a welcome message.

    Returns:
        dict: A JSON object containing a welcome message.
    """
    return {'message': 'Hello World'}

models.Base.metadata.create_all(engine)