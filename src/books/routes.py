from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException ,status, Depends
from .schemas import book, bookupdate , bookcreateModel
from fastapi import APIRouter
from src.db.main import get_session
from .models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService

book_router=APIRouter()
book_service=BookService()

@book_router.get("/",response_model=list[book])
async def get_books(session : AsyncSession = Depends(get_session)):
    books=await book_service.get_all_books(session)
    return books

@book_router.get("/{bookid}",status_code=200)
async def get_book(bookid:str,session : AsyncSession =Depends(get_session)):
    g_book=await book_service.get_book(book_uid=bookid,session=session)
    if g_book:
        return g_book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NOT FOUND")

@book_router.post("/add_book",status_code=201)
async def add_book(book_data: bookcreateModel,session : AsyncSession = Depends(get_session)):
    new_book =await book_service.create_book(book_data,session)
    return new_book

@book_router.put("/updatebook/{book_uid}",status_code=200)
async def updatebook(book_uid:str, book_up :bookupdate,session : AsyncSession =Depends(get_session)):
    updated_book =await book_service.update_book(book_uid,book_up,session)
    if updated_book:
        return updated_book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NOT FOUND")  
    
@book_router.delete("/delete_book/{bookid}", status_code=200)
async def delete_book(bookid: str,session : AsyncSession =Depends(get_session)):
    deleted_book =await book_service.delete_book(bookid,session)
    if deleted_book:
        return deleted_book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NOT FOUND") 