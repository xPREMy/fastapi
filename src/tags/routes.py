from fastapi import APIRouter ,Depends
from src.db.models import Tag
from .schemas import TagBaseModel , TagAddModel, TagCreateModel
from src.auth.dependancies import  RoleChecker
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import TagService
from typing import List
from src.books.schemas import book_review_tags

role_checker = Depends(RoleChecker(['admin', 'user']))
tag_route = APIRouter()
tag_service = TagService()

@tag_route.post("/create_tag",response_model=TagBaseModel,dependencies=[role_checker])
async def create_tag(tag_data : TagCreateModel,session :AsyncSession = Depends(get_session)) -> TagBaseModel:
    return await tag_service.add_tag(tag_data,session)

@tag_route.get("/get_all_tags",response_model=List[TagBaseModel],dependencies=[role_checker])
async def get_all_tags(session :AsyncSession = Depends(get_session)) -> TagBaseModel:
    return await tag_service.get_all_tags(session)

@tag_route.post("/add_tags_to_book/{book_uid}", response_model=book_review_tags,dependencies=[role_checker])
async def add_tag_to_book(book_uid: str, tags : TagAddModel,session :AsyncSession = Depends(get_session))-> book_review_tags:
    return await tag_service.add_tag_to_book(book_uid=book_uid,tags_data=tags,session=session)

@tag_route.delete("/deleted",response_model=TagBaseModel,dependencies=[role_checker])
async def delete_tag(tag: TagCreateModel,session :AsyncSession = Depends(get_session)) -> TagBaseModel:
    return await tag_service.delete_tag(tag,session)