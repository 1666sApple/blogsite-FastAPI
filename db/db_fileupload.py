from fastapi.params import File
from sqlalchemy.orm import Session
from db.models import DBFileUpload, FileType
from datetime import datetime

def createFileRecord(
        db: Session, 
        userID: int, 
        originalFileName: str, 
        storedFileName: str, 
        contentType: FileType, 
        uploadTime: datetime
        ):
    newFile = DBFileUpload(
        userID = userID,
        originalFileName = originalFileName,
        storedFileName = storedFileName,
        contentType = contentType,
        uploadTime = uploadTime
    )
    db.add(newFile)
    db.commit()
    db.refresh(newFile)
    
    return newFile

def getFileByID(db: Session, fileID: int):
    return db.query(DBFileUpload).filter(DBFileUpload.id == fileID).first()

def uploadFileRecord(db: Session, fileID: int, newFileName: str, originalFileName: str, contentType: FileType):
    file = db.query(DBFileUpload).filter(DBFileUpload.id == fileID).first()

    if file:
        file.storedFileName = newFileName
        file.originalFileName = originalFileName
        file.contentType = contentType
        db.commit()
        db.refresh(file)

    return file

def deleteFileRecord(db: Session, fileID: int):
    file = db.query(DBFileUpload).filter(DBFileUpload.id==fileID).first()
    if file:
        db.delete(file)
        db.commit()
