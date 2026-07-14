from fastapi import FastAPI ,Query
from pydantic import BaseModel
from fastapi import HTTPException ,status, Depends
from .schemas import book, bookupdate , bookcreateModel ,book_review
from fastapi import APIRouter
from src.db.main import get_session
from src.db.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService
from src.auth.dependancies import AccessTokenBearer

book_router=APIRouter()
book_service=BookService()
access_token_bearer= AccessTokenBearer()

@book_router.get("/",response_model=list[book])
async def get_books(session : AsyncSession = Depends(get_session), token_details : dict= Depends(access_token_bearer)):
    books=await book_service.get_all_books(session)
    return books

@book_router.get("/user",response_model=list[book])
async def get_user_books(session : AsyncSession = Depends(get_session), token_details : dict= Depends(access_token_bearer)):
    books=await book_service.get_all_user_books(token_details.get('user')["user_uid"],session)
    return books

@book_router.get("/{bookid}",status_code=200,response_model=book_review)
async def get_book(bookid:str,session : AsyncSession =Depends(get_session), token_details : dict= Depends(access_token_bearer)):
    g_book=await book_service.get_book(book_uid=bookid,session=session)
    if g_book:
        return g_book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NOT FOUND")

@book_router.post("/add_book",status_code=201)
async def add_book(book_data: bookcreateModel,session : AsyncSession = Depends(get_session),token_details : dict= Depends(access_token_bearer)):
    user_uid=token_details.get('user')['user_uid']
    new_book =await book_service.create_book(user_uid,book_data,session)
    return new_book

@book_router.put("/updatebook/{book_uid}",status_code=200)
async def updatebook(book_uid:str, book_up :bookupdate,session : AsyncSession =Depends(get_session) ,token_details : dict= Depends(access_token_bearer)):
    updated_book =await book_service.update_book(book_uid,book_up,session)
    if updated_book:
        return updated_book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NOT FOUND")  
    
@book_router.delete("/delete_book/{bookid}", status_code=200)
async def delete_book(bookid: str,session : AsyncSession =Depends(get_session) , token_details : dict= Depends(access_token_bearer)):
    deleted_book =await book_service.delete_book(bookid,session)
    if deleted_book:
        return deleted_book
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="NOT FOUND") 