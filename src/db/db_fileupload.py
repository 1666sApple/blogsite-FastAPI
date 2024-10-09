from email.policy import HTTP
import os
from statistics import median_low
from fastapi.params import File
from sqlalchemy.orm import Session
from src.db.models import DBFileUpload, FileType
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import FileResponse

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
    file = db.query(DBFileUpload).filter(DBFileUpload.id == fileID).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

def getFileByName(db: Session, user_id: int, file_name: str):
    file = db.query(DBFileUpload).filter(
        DBFileUpload.userID == user_id,
        DBFileUpload.storedFileName == file_name
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return file

def getAllUserFiles(db: Session, user_id: int):
    return db.query(DBFileUpload).filter(DBFileUpload.userID == user_id).all()

def uploadFileRecord(db: Session, file_id: int, new_filename: str, originalFileName: str, content_type: FileType):
    file = db.query(DBFileUpload).filter(DBFileUpload.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.storedFileName = new_filename
    file.originalFileName = originalFileName
    file.contentType = content_type
    file.uploadTime = datetime.utcnow()
    db.commit()
    db.refresh(file)

    return file

def deleteFileRecord(db: Session, fileID: int):
    file = db.query(DBFileUpload).filter(DBFileUpload.id == fileID).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    db.delete(file)
    db.commit()
    return {"detail": "File deleted successfully"}

def downloadFileRecord(db: Session, fileID: int, storagePath: str):
    file = db.query(DBFileUpload).filter(DBFileUpload.id == fileID).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    filePath = os.path.join(storagePath, file.storedFileName)

    if not os.path.exists(filePath):
        raise HTTPException(status_code=404, detail="File doesn't exist!")
    
    return FileResponse(
        path=filePath,
        filename=file.originalFileName,
        media_type=file.contentType.value
    )