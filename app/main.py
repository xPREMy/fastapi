from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def f1():
    return {"user_id": "the user"}
