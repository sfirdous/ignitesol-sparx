# Database connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:firdousshamshad@localhost:3306/gutenberg"

engine = create_engine(DATABASE_URL,echo = False)

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db        # database conection to API endpoints
    finally:
        db.close()      # closes connection after use