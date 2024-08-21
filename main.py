from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional

app = FastAPI()

@app.get('/')
def home():
    return {'message':'Hello World'}

@app.get('/blogs/all')
def get_all():
    return {
        'message':'All blogs provided'
    }

@app.get('/blogs')
def get_blog_query(page: int = 1, page_size: Optional[int] = None):
    return {
        'message': f'Fetching blogs, page: {page}, page_size: {page_size}'
    }

@app.get('/blogs/{blog_id}/comments/{comment_id}')
def get_comment(blog_id: int, comment_id: int, valid: bool=True, username: Optional[str] = None):
    return {
        'message': f"blog {blog_id}, comment_id {comment_id}, valid {valid}, username {username}"
    }

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blogs/types/{blog_type}')
def get_blog_type(blog_type: BlogType):
    return {
        'message':f"Fetching blogs of type: {blog_type}"
    }

@app.get("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def get_blog(blog_id: int, response: Response):
    if blog_id > 25:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'error': f"Blog {blog_id} not found"
        }
    else:
        response.status_code = status.HTTP_200_OK
        return {
            'message': f'Fetching blog with id: {blog_id}'
        }