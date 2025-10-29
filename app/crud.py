# Database query functions
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models

def get_books(
    db : Session,
    language : str = None,
    author : str = None,
    topic: str = None,
    title : str = None,
    page : int = 1,
    page_size : int = 25
):
    query = db.query(models.Book)
    
    # apply filters 
    if language:
        query = query.join(models.Book.languages).filter(
            models.Language.code == language
        )
    
    if author:
        query = query.join(models.Book.authors).filter(
            models.Author.name.ilike(f'%{author}%')
        )
    
    if topic:
        query = query.join(models.Book.subjects).filter(
            models.Subject.name.ilike(f'%{topic}%')
        )
    
    if title:
        query = query.filter(
            models.Book.title.ilike(f'%{title}%')
        )
    
    # sort by download count
    query = query.order_by(models.Book.download_count.desc())
    
    # calculate offset for pagination
    offset = (page - 1) * page_size
    
    # apply pagination
    query = query.offset(offset).limit(page_size)
    
    return query.all()

def get_books_count(
    db : Session,
    language : str = None,
    author : str = None,
    topic : str = None,
    title : str = None
):
    """Get total count of books matching filters"""
    query = db.query(models.Book)
    
    if language:
        query = query.join(models.Book.languages).filter(
            models.Language.code == language
        )
    
    if author:
        query = query.join(models.Book.authors).filter(
            models.Author.name.ilike(f'%{author}%')
        )
    
    if topic:
        query = query.join(models.Book.subjects).filter(
            models.Subject.name.ilike(f'%{topic}%')
        )
    
    if title:
        query = query.filter(
            models.Book.title.ilike(f'%{title}%')
        )
    
    return query.count()