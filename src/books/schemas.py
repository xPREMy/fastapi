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

class bookcreateModel(BaseModel):
    name: str