# SQLAlchemy models (database tables)
from sqlalchemy import Column,Integer,String,Text,ForeignKey,Table,SmallInteger
from sqlalchemy.orm import relationship
from .database import Base

book_authors = Table(
    'books_book_authors',
    Base.metadata,
    Column('id',Integer,primary_key=True),
    Column('book_id',Integer,ForeignKey('books_book.id')),
    Column('author_id',Integer,ForeignKey('books_author.id'))
)

book_bookshelves = Table(
    'books_book_bookshelves',
    Base.metadata,
    Column('id',Integer,primary_key=True),
    Column('book_id',Integer,ForeignKey('books_book.id')),
    Column('bookshelf_id',Integer,ForeignKey('books_bookshelf.id'))

)

book_languages = Table(
    'books_book_languages',
    Base.metadata,
    Column('id',Integer,primary_key=True),
    Column('book_id',Integer,ForeignKey('books_book.id')),
    Column('language_id',Integer,ForeignKey('books_language.id'))

)

book_subjects = Table(
    'books_book_subjects',
    Base.metadata,
    Column('id',Integer,primary_key=True),
    Column('book_id',Integer,ForeignKey('books_book.id')),
    Column('subject_id',Integer,ForeignKey('books_subject.id'))

)
class Author(Base):
    """Represents the books_author table"""
    __tablename__ = 'books_author'
    
    id = Column(Integer,primary_key=True)
    birth_year = Column(SmallInteger,nullable = True)
    death_year = Column(SmallInteger,nullable = True)
    name = Column(String(128),nullable = False)
    
    books = relationship(
        'Book',
        secondary=book_authors,
        back_populates='authors'
    )
    
class Book(Base):
    """Represents the books_book table"""
    __tablename__ = 'books_book'
    id = Column(Integer,primary_key=True)
    download_count = Column(Integer,nullable=True)
    gutenberg_id = Column(Integer,nullable=False)
    media_type = Column(String(16),nullable=False)
    title = Column(Text,nullable=True)
    authors = relationship(
        'Author',
        secondary=book_authors,
        back_populates='books'
    )
    subjects = relationship(
        'Subject',
        secondary=book_subjects,
        back_populates='books'
    )
    languages = relationship(
        'Language',
        secondary=book_languages,
        back_populates='books'
    )
    bookshelves = relationship(
        'Bookshelf',
        secondary=book_bookshelves,
        back_populates='books'
    )
    formats = relationship(
        'Format',
        back_populates='book'
    )
    
    
class Subject(Base):
    """Represents the books_subject table"""
    __tablename__ = 'books_subject'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    
    books = relationship(
        'Book',
        secondary=book_subjects,
        back_populates='subjects'
    )


class Language(Base):
    """Represents the books_language table"""
    __tablename__ = 'books_language'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(4), nullable=False)
    books = relationship(
        'Book',
        secondary= book_languages,
        back_populates='languages'
    )


class Format(Base):
    """Represents the books_format table"""
    __tablename__ = 'books_format'
    
    id = Column(Integer, primary_key=True)
    mime_type = Column(String(32), nullable=False)
    url = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('books_book.id'), nullable=False)  
    book = relationship('Book',back_populates='formats')

class Bookshelf(Base):
    """Represents the books_bookshelf table"""
    __tablename__ = 'books_bookshelf'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    books = relationship(
        'Book',
        secondary=book_bookshelves,
        back_populates='bookshelves'
    )
