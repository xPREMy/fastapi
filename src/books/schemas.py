from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List
from src.review.schemas import ReviewBaseModel
from src.db.models import Tag

class book(BaseModel):
    uid : uuid.UUID
    name : str
    user_id : uuid.UUID | None = None
    created_at : datetime
    updated_at : datetime

class book_review(book):
    review : List[ReviewBaseModel]

class book_review_tags(book_review):
    tags : List[Tag]

class bookupdate(BaseModel):
    name: str

class bookcreateModel(BaseModel):
    name: str