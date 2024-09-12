import os
import shutil
import uuid
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from db.db_fileupload import createFileRecord, deleteFileRecord, getFileByID, uploadFileRecord
from db.database import getDB
from schemas import User
from auth import oauth2
from db.models import FileType

router = APIRouter(
    prefix='/file',
    tags=['file']
)

UPLOAD_DIR = 'files/'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def map_content_type(mime_type: str) -> FileType:
    if mime_type.startswith('image/'):
        return FileType.IMAGE
    elif mime_type in ['application/pdf', 'text/plain', 'application/msword']:
        return FileType.DOCUMENT
    elif mime_type.startswith('video/'):
        return FileType.VIDEO
    elif mime_type.startswith('audio/'):
        return FileType.AUDIO
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

def generate_unique_filename(user_id: int, original_filename: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename, extension = os.path.splitext(original_filename)
    return f"{user_id}_{filename}_{timestamp}{extension}"

@router.post('/upload')
def upload_file(
    upload_file: UploadFile = File(...),
    db: Session = Depends(getDB),
    current_user: User = Depends(oauth2.getCurrentUser)
):
    try:
        content_type = map_content_type(upload_file.content_type)
    except HTTPException as e:
        return e

    unique_filename = generate_unique_filename(current_user.id, upload_file.filename)
    path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(path, 'wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    file_record = createFileRecord(
        db=db,
        userID=current_user.id,
        originalFileName=upload_file.filename,
        storedFileName=unique_filename,
        contentType=content_type,
        uploadTime=datetime.utcnow()
    )

    return {"file": upload_file.filename, "unique_file": unique_filename, "type": content_type.value}

@router.get('/{file_id}')
def retrieve_file(file_id: int, db: Session = Depends(getDB)):
    file = getFileByID(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"id": file.id, "original_filename": file.original_filename, "stored_filename": file.stored_filename}

@router.put('/{file_id}')
def modify_file(
    file_id: int,
    upload_file: UploadFile = File(...),
    db: Session = Depends(getDB),
    current_user: User = Depends(oauth2.getCurrentUser)
):
    file = getFileByID(db, file_id)
    if not file or file.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found or not owned by the user")

    # Delete the existing file
    old_path = os.path.join(UPLOAD_DIR, file.stored_filename)
    if os.path.exists(old_path):
        os.remove(old_path)

    # Save the new file with a unique name
    unique_filename = generate_unique_filename(current_user.id, upload_file.filename)
    new_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(new_path, 'wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    updated_file = uploadFileRecord(
        db=db,
        file_id=file_id,
        new_filename=unique_filename,
        original_filename=upload_file.filename,
        content_type=map_content_type(upload_file.content_type)
    )

    return {"id": updated_file.id, "original_filename": updated_file.original_filename, "stored_filename": updated_file.stored_filename}

@router.delete('/{file_id}')
def delete_file(file_id: int, db: Session = Depends(getDB), current_user: User = Depends(oauth2.getCurrentUser)):
    file = getFileByID(db, file_id)
    if not file or file.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found or not owned by the user")

    file_path = os.path.join(UPLOAD_DIR, file.stored_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    deleteFileRecord(db, file_id)
    return {"detail": "File deleted successfully"}