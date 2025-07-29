from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "success"}

@app.post("/post")
def postin(var: dict = Body()):
    print(var)
    return {"goodness": "good"}
