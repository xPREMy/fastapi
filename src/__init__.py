from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_routes
from src.Reviews.routes import Review_route

@asynccontextmanager
async def life_span(app:FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is stopped")

app=FastAPI(
    title="books",
    description="A rest api for book review service"
)
version="v1"
app.include_router(book_router,prefix=f"/books/{version}",tags=['books'])
app.include_router(auth_routes,prefix=f"/users/{version}",tags=['users'])
app.include_router(Review_route,prefix=f"/review/{version}",tags=['review'])