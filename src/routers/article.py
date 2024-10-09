from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.oauth2 import getCurrentUser
from src.db import db_article
from src.db.database import getDB
from src.schemas import ArticleBase, ArticleDisplay, UserBase
from src.exception import TermsViolationException

router = APIRouter(
    prefix='/article',
    tags=['article']
)

@router.post('/', response_model=ArticleDisplay)
def create_article(
    request: ArticleBase,
    db: Session = Depends(getDB),
    current_user: UserBase = Depends(getCurrentUser)
):
    request.userID = current_user.id
    article = db_article.createArticle(db, request)
    if not article:
        raise HTTPException(status_code=400, detail="Article already exists")
    return db_article.getArticle(db, article.id)

@router.get('/', response_model=List[ArticleDisplay])
def get_All_Articles(db: Session = Depends(getDB), current_user: UserBase = Depends(getCurrentUser)):
    return db_article.getAllArticle(db)

@router.get('/{id}', response_model=ArticleDisplay)
def read_One_Article(
    id: int,
    db: Session = Depends(getDB),
    current_user: UserBase = Depends(getCurrentUser)
):
    article = db_article.getArticle(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.userID != current_user.id:
        raise TermsViolationException("You are not authorized to access this article. This action has been marked as a terms violation.")
    return article

@router.put('/{id}/update', response_model=ArticleDisplay)
def update_Article(
    id: int,
    request: ArticleBase,
    db: Session = Depends(getDB),
    current_user: UserBase = Depends(getCurrentUser)
):
    existing_article = db_article.getArticle(db, id)
    if not existing_article:
        raise HTTPException(status_code=404, detail="No article found to update")
    if existing_article.userID != current_user.id:
        raise TermsViolationException("You are not authorized to update this article. This action has been marked as a terms violation.")
    
    updated_article = db_article.updateArticle(db, id, request)
    return updated_article

@router.delete('/{id}/delete')
def delete_Article(
    id: int,
    db: Session = Depends(getDB),
    current_user: UserBase = Depends(getCurrentUser)
):
    existing_article = db_article.getArticle(db, id)
    if not existing_article:
        raise HTTPException(status_code=404, detail="No article found to delete")
    if existing_article.userID != current_user.id:
        raise TermsViolationException("You are not authorized to delete this article. This action has been marked as a terms violation.")
    
    result = db_article.deleteArticle(db, id)
    return {"message": result}
