# Database query functions
from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models,schemas

products = [
    schemas.ProductSchema(id=2,name='xyz',description = 'test'),
    schemas.ProductSchema(id=6,name='2xyz',description = '2test'),
    schemas.ProductSchema(id=8,name='3xyz',description = '3test'),
]
def get_products_by_id(id : int):
    for product in products:
        if product.id == id:
            return product
        
def add_product(product:schemas.ProductSchema):
    products.append(product)

def get_books(
    db: Session,
    book_id: str = None,
    language: str = None,
    mime_type: str = None,
    author: str = None,
    topic: str = None,
    title: str = None,
    page: int = 1,
    page_size: int = 25
):
    """Get books with optional filters.
    Returns:
        List of Book objects matching the filters
    """
    query = db.query(models.Book).distinct()
    
    # Filter by book ID(s)
    if book_id:
        book_ids = [int(id.strip()) for id in book_id.split(',')]
        query = query.filter(models.Book.id.in_(book_ids))
    
    # Filter by language(s)
    if language:
        languages = [lang.strip() for lang in language.split(',')]
        query = query.join(models.Book.languages).filter(
            models.Language.code.in_(languages)
        )
    
    # Filter by MIME type(s)
    if mime_type:
        mime_types = [mt.strip() for mt in mime_type.split(',')]
        query = query.join(models.Book.formats).filter(
            models.Format.mime_type.in_(mime_types)
        )
    
    # Filter by author (partial match, case-insensitive)
    if author:
        authors = [a.strip() for a in author.split(',')]
        author_conditions = [
            models.Author.name.ilike(f'%{a}%') for a in authors
        ]
        query = query.join(models.Book.authors).filter(
            or_(*author_conditions)
        )
    
    # Filter by topic (search in BOTH subjects AND bookshelves)
    if topic:
        topics = [t.strip() for t in topic.split(',')]
        
        # Create conditions for subjects
        subject_conditions = [
            models.Subject.name.ilike(f'%{t}%') for t in topics
        ]
        
        # Create conditions for bookshelves
        bookshelf_conditions = [
            models.Bookshelf.name.ilike(f'%{t}%') for t in topics
        ]
        
        # Join with subjects and bookshelves, filter on either
        query = query.outerjoin(models.Book.subjects).outerjoin(models.Book.bookshelves).filter(
            or_(
                or_(*subject_conditions),
                or_(*bookshelf_conditions)
            )
        )
    
    # Filter by title (partial match, case-insensitive)
    if title:
        titles = [t.strip() for t in title.split(',')]
        title_conditions = [
            models.Book.title.ilike(f'%{t}%') for t in titles
        ]
        query = query.filter(or_(*title_conditions))
    
    # Sort by download count (descending - most popular first)
    query = query.order_by(models.Book.download_count.desc())
    
    # Calculate offset for pagination
    offset = (page - 1) * page_size
    
    # Apply pagination
    query = query.offset(offset).limit(page_size)
    
    return query.all()


def get_books_count(
    db: Session,
    book_id: str = None,
    language: str = None,
    mime_type: str = None,
    author: str = None,
    topic: str = None,
    title: str = None
):
    """
    Get total count of books matching filters
    Returns:
        Integer count of matching books
    """
    query = db.query(models.Book).distinct()
    
    # Filter by book ID(s)
    if book_id:
        book_ids = [int(id.strip()) for id in book_id.split(',')]
        query = query.filter(models.Book.id.in_(book_ids))
    
    # Filter by language(s)
    if language:
        languages = [lang.strip() for lang in language.split(',')]
        query = query.join(models.Book.languages).filter(
            models.Language.code.in_(languages)
        )
    
    # Filter by MIME type(s)
    if mime_type:
        mime_types = [mt.strip() for mt in mime_type.split(',')]
        query = query.join(models.Book.formats).filter(
            models.Format.mime_type.in_(mime_types)
        )
    
    # Filter by author (partial match, case-insensitive)
    if author:
        authors = [a.strip() for a in author.split(',')]
        author_conditions = [
            models.Author.name.ilike(f'%{a}%') for a in authors
        ]
        query = query.join(models.Book.authors).filter(
            or_(*author_conditions)
        )
    
    # Filter by topic (search in BOTH subjects AND bookshelves)
    if topic:
        topics = [t.strip() for t in topic.split(',')]
        
        subject_conditions = [
            models.Subject.name.ilike(f'%{t}%') for t in topics
        ]
        
        bookshelf_conditions = [
            models.Bookshelf.name.ilike(f'%{t}%') for t in topics
        ]
        
        query = query.outerjoin(models.Book.subjects).outerjoin(models.Book.bookshelves).filter(
            or_(
                or_(*subject_conditions),
                or_(*bookshelf_conditions)
            )
        )
    
    # Filter by title (partial match, case-insensitive)
    if title:
        titles = [t.strip() for t in title.split(',')]
        title_conditions = [
            models.Book.title.ilike(f'%{t}%') for t in titles
        ]
        query = query.filter(or_(*title_conditions))
    
    return query.count()
