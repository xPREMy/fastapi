from fastapi import FastAPI
from src.books.routes import book_router

app=FastAPI(
    title="books",
    description="A rest api for book review service"
)
version="v1"
app.include_router(book_router,prefix=f"/books/{version}",tags=['books'])
