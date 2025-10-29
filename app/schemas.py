# Pydantic models (API responses)
from pydantic import BaseModel
from typing import Optional,List

class AuthorSchema(BaseModel):
    name : Optional[str] = None
    birth_year : Optional[int] = None
    death_year : Optional[int] = None

    class Config:
        from_attributes = True

class SubjectSchema(BaseModel):
    name : str
    
    class Config:
        from_attributes = True

class LanguageSchema(BaseModel):
    code : str
    
    class Config:
        from_attributes = True

class FormatSchema(BaseModel):
    mime_type : str
    url : str
    
    class Config:
        from_attributes = True

class BookshelfSchema(BaseModel):
     name : str
     
     class Config:
        from_attributes = True
     
class BookSchema(BaseModel):
    id : int
    download_count : Optional[int] = None
    gutenberg_id : int
    media_type : str
    title : Optional[str] = None
    authors : List[AuthorSchema] = []
    subjects : List[SubjectSchema] = []
    languages : List[LanguageSchema] = []
    bookshelves : List[BookshelfSchema] = []
    formats : List[FormatSchema] = []
    
    class Config:
        from_attributes = True

class BookListResponse(BaseModel):
    """Response for book list with pagination info"""
    count : int
    page : int
    page_size : int
    total_pages : int
    results : List[BookSchema]
