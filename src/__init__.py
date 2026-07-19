from fastapi import FastAPI ,status
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_routes
from src.review.routes import Review_route
from src.tags.routes import tag_route
from .errors import *
from .middleware import register_middleware

app=FastAPI(
    title="books",
    description="A rest api for book review service"
)
version="v1"
register_all_errors(app)
register_middleware(app)

app.include_router(book_router,prefix=f"/books/{version}",tags=['books'])
app.include_router(auth_routes,prefix=f"/users/{version}",tags=['users'])
app.include_router(Review_route,prefix=f"/review/{version}",tags=['review'])
app.include_router(tag_route,prefix=f"/tag/{version}",tags=['tag'])