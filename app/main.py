# FastAPI app initialization
from dotenv import load_dotenv
from app.database import engine
from app.models import Base
from fastapi import FastAPI
from .routers import books

load_dotenv()

app = FastAPI(
    title="Gutenberg Books API",
    description="API for browsing Project Gutenberg books",
    version="1.0.0"
)

# include the books router
app.include_router(books.router)
@app.get("/")
def root():
    return {"message":"Welcome to Gutenberg Books API. Visit /docs for documentation."}
    

Base.metadata.create_all(bind = engine)


