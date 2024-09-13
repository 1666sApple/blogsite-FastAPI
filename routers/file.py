import os
import shutil
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from db.db_fileupload import createFileRecord, deleteFileRecord, getFileByName, getFileByID, uploadFileRecord, getAllUserFiles
from db.database import getDB
from schemas import User, FileResponse
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

def generate_filename(user_id: int, custom_filename: str) -> str:
    return f"{custom_filename}"

@router.post('/upload')
def upload_file(
    upload_file: UploadFile = File(...),
    custom_filename: str = None,
    db: Session = Depends(getDB),
    current_user: User = Depends(oauth2.getCurrentUser)
):
    try:
        content_type = map_content_type(upload_file.content_type)
    except HTTPException as e:
        return e

    if not custom_filename:
        raise HTTPException(status_code=400, detail="Custom filename is required")

    filename = generate_filename(current_user.id, custom_filename)
    path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(path):
        raise HTTPException(status_code=400, detail="File with this name already exists")

    with open(path, 'wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    file_record = createFileRecord(
        db=db,
        userID=current_user.id,
        originalFileName=custom_filename,
        storedFileName=filename,
        contentType=content_type,
        uploadTime=datetime.utcnow()
    )

    return {"file": custom_filename, "stored_file": filename, "type": content_type.value}

@router.get('/list', response_model=List[FileResponse])
def list_user_files(db: Session = Depends(getDB), current_user: User = Depends(oauth2.getCurrentUser)):
    files = getAllUserFiles(db, current_user.id)
    return [
        FileResponse(
            id=file.id,
            originalFileName=file.originalFileName,
            contentType=file.contentType.value,
            uploadTime=file.uploadTime
        ) for file in files
    ]

@router.get('/{file_name}')
def retrieve_file(file_name: str, db: Session = Depends(getDB), current_user: User = Depends(oauth2.getCurrentUser)):
    file = getFileByName(db, current_user.id, file_name)
    if not file:
        raise HTTPException(status_code=404, detail="File not found or not owned by the user")
    
    return FileResponse(
        id=file.id,
        originalFileName=file.originalFileName,
        contentType=file.contentType.value,
        uploadTime=file.uploadTime
    )

@router.put('/{file_name}')
def modify_file(
    file_name: str,
    upload_file: UploadFile = File(...),
    custom_filename: str = None,
    db: Session = Depends(getDB),
    current_user: User = Depends(oauth2.getCurrentUser)
):
    file = getFileByName(db, current_user.id, file_name)
    if not file:
        raise HTTPException(status_code=404, detail="File not found or not owned by the user")

    # Delete the existing file
    old_path = os.path.join(UPLOAD_DIR, file.storedFileName)
    if os.path.exists(old_path):
        os.remove(old_path)

    # Use custom filename if provided, otherwise use the original uploaded file's name
    if not custom_filename:
        custom_filename = upload_file.filename

    new_filename = generate_filename(current_user.id, custom_filename)
    new_path = os.path.join(UPLOAD_DIR, new_filename)

    # Save the new file
    with open(new_path, 'wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # Update the file record
    updated_file = uploadFileRecord(
        db=db,
        file_id=file.id,
        new_filename=new_filename,
        originalFileName=upload_file.filename,
        content_type=map_content_type(upload_file.content_type)
    )

    return {"id": updated_file.id, "originalFileName": updated_file.originalFileName, "storedFileName": updated_file.storedFileName}

@router.delete('/{file_name}')
def delete_file(file_name: str, db: Session = Depends(getDB), current_user: User = Depends(oauth2.getCurrentUser)):
    file = getFileByName(db, current_user.id, file_name)
    if not file:
        raise HTTPException(status_code=404, detail="File not found or not owned by the user")

    file_path = os.path.join(UPLOAD_DIR, file.storedFileName)
    if os.path.exists(file_path):
        os.remove(file_path)

    deleteFileRecord(db, file.id)
    return {"detail": "File deleted successfully"}

@router.get('/download/{file_name}')
def download_file(file_name: str, db: Session = Depends(getDB), current_user: User = Depends(oauth2.getCurrentUser)):
    file = getFileByName(db, current_user.id, file_name)
    if not file:
        raise HTTPException(status_code=404, detail="File not found or not owned by the user")
    
    file_path = os.path.join(UPLOAD_DIR, file.storedFileName)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FastAPIFileResponse(
        path=file_path,
        filename=file.originalFileName,
        media_type=file.contentType.value
    )