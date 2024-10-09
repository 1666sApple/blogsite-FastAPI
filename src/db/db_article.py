from sqlalchemy.orm import Session, joinedload
from src.db.models import DBarticles, DBusers
from src.exception import StoryException
from src.schemas import ArticleBase

def createArticle(db: Session, request: ArticleBase):
    if request.content.startswith('Once Upon a time'):
        raise StoryException('No stories allowed')
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
    return db.query(DBarticles).options(joinedload(DBarticles.user)).all()
    
def getArticle(db: Session, id: int):
    return db.query(DBarticles).options(joinedload(DBarticles.user)).filter(DBarticles.id == id).first()

def updateArticle(db: Session, id: int, request: ArticleBase):
    article = db.query(DBarticles).filter(DBarticles.id == id).first()
    
    if not article:
        return None
        
    article.title = request.title
    article.content = request.content
    article.published = request.published
    
    db.commit()
    db.refresh(article)
    return getArticle(db, id)
    
def deleteArticle(db: Session, id: int):
    article = db.query(DBarticles).filter(DBarticles.id == id).first()
    
    if not article:
        return "No article found to delete."
    
    db.delete(article)
    db.commit()
    return 'Article deleted successfully.'