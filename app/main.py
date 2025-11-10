# FastAPI app initialization
from dotenv import load_dotenv      # imports function that loads environment variables from .env file into system's environment variables
load_dotenv()                       # calls .env file and loads all key-value pairs into environment variables making them accessible via os.

from app.database import engine
from app.models import Base
from fastapi import FastAPI
from .routers import books,products


app = FastAPI(
    title="Gutenberg Books API",
    description="API for browsing Project Gutenberg books",
    version="1.0.0"
)

# include the books router
app.include_router(books.router)
app.include_router(products.router)
@app.get("/")
def read_root():
    return {"message":"Welcome to Gutenberg Books API. Visit /docs for documentation."}




Base.metadata.create_all(bind = engine)


