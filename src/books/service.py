from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import bookcreateModel,bookupdate
from sqlmodel import select,desc
from .models import Book

class BookService:
    async def get_all_books(self, session : AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result= await session.exec(statement)
        return result.all()

    async def get_book(self,book_uid:str, session : AsyncSession):
        statement = select(Book).where(Book.uid==book_uid)
        result=await session.exec(statement)
        book= result.first()
        if book is not None:
            return book
        return None
    
    async def create_book(self,book_data:bookcreateModel,session : AsyncSession):
        book_data_dict=book_data.model_dump()
        new_book=Book(
            **book_data_dict
            )
        session.add(new_book)
        await session.commit()
        return new_book
    async def update_book(self,book_uid:str,book_data:bookupdate,session : AsyncSession):
        book_to_update=self.get_book(book_uid=book_uid)
        if book_to_update is not None:
            update_data_dict=book_data.model_dump()
            for k , v in update_data_dict.items():
                setattr(book_to_update,k,v)
            await session.commit()
            return book_to_update
        return None
    async def delete_book(self,book_uid:str,session : AsyncSession):
        book_to_delete=self.get_book(book_uid)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
        else :
            return None