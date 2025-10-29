# API Endpoints
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import crud,schemas
from ..database import get_db
import math

router = APIRouter(
    prefix="/books",
    tags = ["books"]
)

@router.get("/",response_model=schemas.BookListResponse)
def get_books(
    language : Optional[str] = Query(None,description="Filter by language code"),
    author : Optional[str] = Query(None,description="Filter by author name"),
    topic : Optional[str] = Query(None,description="Filter by subject/topic"),
    title : Optional[str] = Query(None,description="Filter by book title"),
    page : int = Query(1,ge=1,description="Page number starts at 1"),
    db : Session = Depends(get_db)
):
    """Get books with optional filters and pagination
    Returns 25 books per page, sorted by download count"""
    
    # get the books
    books = crud.get_books(
        db = db,
        language=language,
        author=author,
        topic=topic,
        title=title, 
        page = page  
    )
    
    page_size = 25
    # get total count
    total_count = crud.get_books_count(
        db = db,
        language=language,
        author=author,
        topic=topic,
        title=title
    )
    total_pages = math.ceil(total_count/page_size)
    
    
    return { "count" : total_count,
            "page" : page,
            "page_size" : page_size,
            "total_pages" : total_pages,
            "results" : books
    }
    