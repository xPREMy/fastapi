from pydantic import BaseModel , Field
from datetime import datetime
import uuid

class UserModel(BaseModel):
    uid : uuid.UUID 
    username: str
    email : str
    is_verified : bool
    Password_hash : str 
    created_at : datetime 
    updated_at : datetime 

class Usercreatemodel(BaseModel):
    username : str= Field(max_length=10)
    email : str
    password : str = Field(min_length=8)
    