from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class ReviewBaseModel(BaseModel):
    uid : uuid.UUID
    rating : int
    description : str
    user_id : uuid.UUID
    book_id : uuid.UUID
    created_at : datetime
    updated_at : datetime

class ReviewCreateModel(BaseModel):
    rating : int
    description : str

class ReviewEditModel(BaseModel):
    description : str
    