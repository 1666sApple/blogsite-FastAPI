from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from auth.oauth2 import oauth2Scheme
from db import db_article
from db.database import getDB
from schemas import ArticleBase, ArticleDisplay

router = APIRouter(
    prefix='/article',
    tags=['article']
)

@router.post('/', response_model=ArticleDisplay)
def createArticle(request: ArticleBase, db: Session = Depends(getDB), token: str = Depends(oauth2Scheme)):
    article = db_article.createArticle(db, request)
    if not article:
        raise HTTPException(status_code=400, detail="Article already exists")
    
    return article

@router.get('/', response_model=List[ArticleDisplay])
def getAllArticles(db: Session = Depends(getDB)):
    return db_article.getAllArticle(db)

@router.get('/{id}', response_model=ArticleDisplay)
def readOneArticle(id: int, db: Session = Depends(getDB), token: str = Depends(oauth2Scheme)):
    article = db_article.getArticle(db, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
    
@router.put('/{id}/update', response_model=ArticleDisplay)
def updateArticle(id: int, request: ArticleBase, db: Session = Depends(getDB), token: str = Depends(oauth2Scheme)):
    article = db_article.updateArticle(db, id, request)
    if not article:
        raise HTTPException(status_code=404, detail="No article found to update")
    return article
    
@router.delete('/{id}/delete')
def deleteArticle(id: int, db: Session = Depends(getDB), token: str = Depends(oauth2Scheme)):
    result = db_article.deleteArticle(db, id)
    if result == "No article found to delete.":
        raise HTTPException(status_code=404, detail=result)
    return {"message": result} 