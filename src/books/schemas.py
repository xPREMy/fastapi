from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List
from src.Reviews.schemas import ReviewBaseModel

class book(BaseModel):
    uid : uuid.UUID
    name : str
    user_id : uuid.UUID | None = None
    created_at : datetime
    updated_at : datetime

class book_review(book):
    reviews = List[ReviewBaseModel]

class bookupdate(BaseModel):
    name: str

class bookcreateModel(BaseModel):
    name: str