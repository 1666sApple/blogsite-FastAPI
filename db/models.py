from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from db.database import Base
from sqlalchemy import Column, DateTime, Enum
from enum import Enum as PyEnum
class DBusers(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    items = relationship('DBarticles', back_populates='user')
    files = relationship('DBFileUpload', back_populates = 'user')

class DBarticles(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    userID = Column(Integer, ForeignKey('users.id'))
    user = relationship('DBusers', back_populates='items')

class FileType(PyEnum):
    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    
class DBFileUpload(Base):
    __tablename__ = 'file_upload'

    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.id"))
    originalFileName = Column(String, nullable=False)
    storedFileName = Column(String, nullable=False)
    contentType = Column(Enum(FileType), nullable = False)
    uploadTime = Column(DateTime, nullable=False)
    user = relationship('DBusers', back_populates='files')