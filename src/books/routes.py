from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException ,status
from src.books.books_data import books
from src.books.schemas import book, bookupdate
from fastapi import APIRouter
book_router=APIRouter()

@book_router.get("/")
def get_book():
    return books
@book_router.get("/{bookid}",status_code=200)
def get_book(bookid:int):
    for i in books:
        if i["id"]==bookid:
            return i
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

@book_router.post("/add_book",status_code=201)
def add_book(book : book):
    newbook=book.model_dump()
    books.append(newbook)


@book_router.put("/updatebook/{bookid}",status_code=200)
def updatebook(bookid:int, bookup :bookupdate):
    for book in books:
        if book["id"]==bookid:
            book["name"]=bookup.name
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="book not found"
    )    
    
@book_router.delete("/delete_book/{bookid}", status_code=200)
def delete_book(bookid: int):
    for i, book in enumerate(books):
        if book["id"] == bookid:
            books.pop(i)
            return {"message": "book deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="book not found"
    )
