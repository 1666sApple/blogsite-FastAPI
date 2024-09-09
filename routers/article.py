from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.oauth2 import getCurrentUser
from db import db_article
from db.database import getDB
from schemas import ArticleBase, ArticleDisplay, UserBase
from exception import TermsViolationException

router = APIRouter(
    prefix='/article',
    tags=['article']
)

@router.post('/', response_model=ArticleDisplay)
def createArticle(
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
def getAllArticles(db: Session = Depends(getDB), current_user: UserBase = Depends(getCurrentUser)):
    return db_article.getAllArticle(db)

@router.get('/{id}', response_model=ArticleDisplay)
def readOneArticle(
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
def updateArticle(
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
def deleteArticle(
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
