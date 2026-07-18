from sqlmodel import SQLModel , select , desc 
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Tag
from fastapi import status
from .schemas import TagAddModel , TagCreateModel
from src.books.service import BookService
from src.errors import *

book_service = BookService()

class TagService(SQLModel):
    async def get_all_tags(self,session : AsyncSession):
        statement = select(Tag).order_by(desc(Tag.created_at))
        result = await session.exec(statement=statement)
        return result.all()
    
    async def get_tag(self,tag : str , session : AsyncSession):
        statement = select(Tag).where(Tag.tag_name==tag)
        result = await session.exec(statement=statement)
        TAG = result.first()
        return TAG
    
    async def add_tag(self, tag : TagCreateModel,session : AsyncSession):
        TAG = await self.get_tag(tag.tag_name,session=session)
        if TAG is not None :
            raise TagAlreadyExists()
        tag_dict= tag.model_dump()
        TAG = Tag(
            **tag_dict
        )
        session.add(TAG)
        await session.commit()
        await session.refresh(TAG)
        return TAG
    
    async def add_tag_to_book(self, book_uid : str , tags_data : TagAddModel,session : AsyncSession):
        book = await book_service.get_book(book_uid=book_uid,session=session)
        if book is None:
            raise BookNotFound()
        for tags in tags_data.tags :
            TAG = await self.get_tag(tags.tag_name,session)
            if TAG is None:
                TAG= Tag(tag_name=tags.tag_name)
                session.add(TAG)
                await session.commit()
                await session.refresh(TAG)
            book.tags.append(TAG)

        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    
    async def delete_tag(self,tag : TagCreateModel , session : AsyncSession):
        TAG = await self.get_tag(tag.tag_name,session)
        if TAG is None :
            raise TagNotFound()
        session.delete(TAG)
        await session.commit()
        return TAG

    
