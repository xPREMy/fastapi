from pydantic import BaseModel
class book(BaseModel):
    id : int
    name : str

class bookupdate(BaseModel):
    name: str
