from sqlalchemy.orm import Session
from db.models import DBarticles
from exception import StoryException
from schemas import ArticleBase

def createArticle(db: Session, request: ArticleBase):
    if request.content.startswith('Once Upon a time'):
        raise StoryException
    existing_article = db.query(DBarticles).filter(DBarticles.title == request.title).first()
    if existing_article:
        return None
    
    newArticle = DBarticles(
        title=request.title,
        content=request.content,
        published=request.published,
        userID=request.userID,
    )
    
    db.add(newArticle)
    db.commit()
    db.refresh(newArticle)
    
    return newArticle  

def getAllArticle(db: Session):
    return db.query(DBarticles).all()
    
def getArticle(db: Session, id: int):
    return db.query(DBarticles).filter(DBarticles.id == id).first()

def updateArticle(db: Session, id: int, request: ArticleBase):
    article = db.query(DBarticles).filter(DBarticles.id == id).first()
    
    if not article:
        return None
        
    article.title = request.title
    article.content = request.content
    article.published = request.published
    article.userID = request.userID
    
    db.commit()
    db.refresh(article)
    return article  # Return the updated article object
    
def deleteArticle(db: Session, id: int):
    article = db.query(DBarticles).filter(DBarticles.id == id).first()
    
    if not article:
        return "No article found to delete."
    
    db.delete(article)
    db.commit()
    return 'Article deleted successfully.'