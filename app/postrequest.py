from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class post(BaseModel):
    title : str
    discription: str 
    public : bool = True
    rating : Optional[int] = None

@app.get("/")
def root():
    return {"message": "success"}

@app.post("/post")
def postin(var : post):
    print(var)
    return {"goodness": var}
