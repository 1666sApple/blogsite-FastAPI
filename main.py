from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth import authentication
from exception import StoryException, TermsViolationException
from routers import article, user, blog_get, blog_post
from db import models
from db.database import engine


app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(article.router)



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