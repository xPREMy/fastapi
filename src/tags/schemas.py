from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List
from src.db.models import Book

class TagBaseModel(BaseModel):
    uid : uuid.UUID
    tag_name : str
    created_at : datetime

class TagCreateModel(BaseModel):
    tag_name : str

class TagAddModel(BaseModel):
    tags : List[TagCreateModel]