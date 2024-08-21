from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional

app = FastAPI()

@app.get(
    '/',
    summary="Home Endpoint", 
    description="Returns a welcome message."
    )
def home():
    return {'message': 'Hello World'}

@app.get(
    '/blogs/all', 
    tags=['blog'], 
    summary="Get All Blogs", 
    description="Retrieve a message indicating that all blogs are provided."
    )
def get_all():
    return {
        'message': 'All blogs provided'
    }

@app.get(
    '/blogs', 
    tags=['blog'], 
    summary="Get Blogs with Pagination", 
    description="Fetch a list of blogs with pagination options."
    )
def get_blog_query(page: int = 1, page_size: Optional[int] = None):
    return {
        'message': f'Fetching blogs, page: {page}, page_size: {page_size}'
    }

@app.get(
    '/blogs/{blog_id}/comments/{comment_id}', 
    tags=['blog', 'comment'], 
    summary="Get Blog Comments", 
    description="Retrieve a specific comment for a given blog by its ID."
    )
def get_comment(blog_id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {
        'message': f"blog {blog_id}, comment_id {comment_id}, valid {valid}, username {username}"
    }

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get(
    '/blogs/types/{blog_type}', 
    tags=['blog', 'type'], 
    summary="Get Blogs by Type", 
    description="Fetch blogs of a specific type such as short, story, or how-to."
    )
def get_blog_type(blog_type: BlogType):
    return {
        'message': f"Fetching blogs of type: {blog_type}"
    }

@app.get(
    "/blogs/{blog_id}", 
    status_code=status.HTTP_200_OK, 
    tags=['blog'], 
    summary="Get Blog by ID", 
    description="Retrieve a specific blog by its ID. Returns a 404 error if the blog is not found."
    )
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