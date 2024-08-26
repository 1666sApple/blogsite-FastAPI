from fastapi import FastAPI, APIRouter, Query, Body, Path
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()
router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool] = None

@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int):
    """
    Create a new blog post.
    
    - **id**: Unique identifier for the blog post.
    - **version**: Version number of the blog post.
    - **blog**: BlogModel containing the blog details.
    """
    return {
        'id': id,
        'data': blog,
        'version': version
    }
    
@router.post('/new/{id}/comment/{comment_id}')
def create_comment(
    id: int,
    comment_title: str = Query(...,
        title='Title of the comment',
        description='Description for the comment',
        alias='commentTitle'
    ),
    content: str = Body(
        ...,
        min_length=10,
        max_length=50
    ),
    version: Optional[List[str]] = Query(['1.0', '1.1', '1.2', '1.3', '1.4', '1.5']),
    blog: BlogModel = Body(...),
    comment_id: int = Path(..., gt=5, le=10)
):
    """
    Create a new comment for a blog post.
    
    - **id**: Unique identifier for the blog post.
    - **comment_id**: Unique identifier for the comment.
    - **content**: The content of the comment (10-50 characters).
    - **version**: Optional list of version identifiers.
    - **blog**: BlogModel containing the blog details.
    """
    return {
        'blog': blog,
        'blog_id': id,
        'comment_title': comment_title,
        'content': content,
        'version': version
    }