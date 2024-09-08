from math import prod
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from auth import authentication
from exception import StoryException
from routers import article, blog_get, blog_post, user
from db import models
from db.database import engine

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(authentication.router)


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

@app.exception_handler(StoryException)
def storyExceptionHandler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={
            'detail' : exc.name
            }
    )

@app.exception_handler(HTTPException)
def customHandler(request: Request, exc: StoryException):
    return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(engine)