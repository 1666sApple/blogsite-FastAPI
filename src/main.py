from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.auth import authentication
from src.exception import StoryException, TermsViolationException
from src.routers import article, file, user, blog_get, blog_post
from src.db import models
from src.db.database import engine


app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(article.router)
app.include_router(file.router)

@app.exception_handler(StoryException)
def storyExceptionHandler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={"detail": exc.name}
    )

@app.exception_handler(TermsViolationException)
def termsViolationExceptionHandler(request: Request, exc: TermsViolationException):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc.detail), "terms_violation": True}
    )

models.Base.metadata.create_all(engine)