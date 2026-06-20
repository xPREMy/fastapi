from pydantic import BaseModel
import uuid
from datetime import datetime
class book(BaseModel):
    uid : uuid.UUID
    name : str
    created_at : datetime
    updated_at : datetime
class bookupdate(BaseModel):
    name: str
    updated_at : datetime

class bookcreateModel(BaseModel):
    name: str
    created_at : datetime
    updated_at : datetime