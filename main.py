from fastapi import FastAPI, status, Response
from enum import Enum
from typing import Optional

app = FastAPI()

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

@app.get(
    '/blogs/all', 
    tags=['blog'], 
    summary="Get All Blogs", 
    description="Retrieve a message indicating that all blogs are provided.",
    response_description="A JSON object confirming that all blogs are provided."
)
def get_all():
    """
    Retrieve a message indicating that all blogs are available.

    Returns:
        dict: A JSON object with a message confirming that all blogs are provided.
    """
    return {
        'message': 'All blogs provided'
    }

@app.get(
    '/blogs', 
    tags=['blog'], 
    summary="Get Blogs with Pagination", 
    description="Fetch a list of blogs with pagination options.",
    response_description="A JSON object containing the page number and page size."
)
def get_blog_query(page: int = 1, page_size: Optional[int] = None):
    """
    Fetch a list of blogs with pagination.

    Parameters:
        page (int): The page number to retrieve (default is 1).
        page_size (Optional[int]): The number of blogs per page (default is None).

    Returns:
        dict: A JSON object containing the page number and page size.
    """
    return {
        'message': f'Fetching blogs, page: {page}, page_size: {page_size}'
    }

@app.get(
    '/blogs/{blog_id}/comments/{comment_id}', 
    tags=['blog', 'comment'], 
    summary="Get Blog Comments", 
    description="Retrieve a specific comment for a given blog by its ID.",
    response_description="A JSON object containing the blog ID, comment ID, validity, and username."
)
def get_comment(blog_id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Retrieve a specific comment for a given blog.

    Parameters:
        blog_id (int): The ID of the blog.
        comment_id (int): The ID of the comment.
        valid (bool): Indicates whether the comment is valid (default is True).
        username (Optional[str]): The username of the commenter (default is None).

    Returns:
        dict: A JSON object containing the blog ID, comment ID, validity, and username.
    """
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
    description="Fetch blogs of a specific type such as short, story, or how-to.",
    response_description="A JSON object indicating the type of blogs being fetched."
)
def get_blog_type(blog_type: BlogType):
    """
    Fetch blogs of a specific type.

    Parameters:
        blog_type (BlogType): The type of blog to fetch (short, story, howto).

    Returns:
        dict: A JSON object indicating the type of blogs being fetched.
    """
    return {
        'message': f"Fetching blogs of type: {blog_type}"
    }

@app.get(
    "/blogs/{blog_id}", 
    status_code=status.HTTP_200_OK, 
    tags=['blog'], 
    summary="Get Blog by ID", 
    description="Retrieve a specific blog by its ID. Returns a 404 error if the blog is not found.",
    response_description="A JSON object containing the blog ID if found, or an error message if not found."
)
def get_blog(blog_id: int, response: Response):
    """
    Retrieve a specific blog by its ID.

    Parameters:
        blog_id (int): The ID of the blog to retrieve.

    Returns:
        dict: A JSON object containing the blog ID if found, or an error message if not found.
    """
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