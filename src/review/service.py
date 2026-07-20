from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select ,desc
from src.db.models import Review ,User
from .schemas import ReviewBaseModel , ReviewEditModel , ReviewCreateModel
from src.auth.service import Userservice
from src.books.service import BookService
from src.errors import BookNotFound, BookException
from fastapi import HTTPException ,status

user_service = Userservice()
book_service = BookService()

class ReviewService:
    async def add_review_to_book(self,user : User ,book_uid : str,rev : ReviewCreateModel ,session : AsyncSession):
        try:
            book=await book_service.get_book(book_uid=book_uid,session=session)
            if book is None:
                raise BookNotFound()
            rev_dict = rev.model_dump()
            new_review = Review(
                **rev_dict
            )
            new_review.user_id=user.uid
            new_review.book_id=book_uid
            new_review.user=user
            new_review.book=book
            session.add(new_review)
            await session.commit()
            await session.refresh(new_review)
            return new_review
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops... something went wrong")
        
    
