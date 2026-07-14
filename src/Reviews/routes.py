from fastapi import APIRouter ,Depends
from .schemas import ReviewCreateModel
from src.db.models import User
from src.auth.dependancies import get_current_user
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import ReviewService

review_service=ReviewService()
Review_route = APIRouter()

@Review_route.post("/book/{book_uid}")
async def add_review(book_uid:str,rev : ReviewCreateModel,user : User = Depends(get_current_user),session : AsyncSession = Depends(get_session)):
    return await review_service.add_review_to_book(user,book_uid,rev)