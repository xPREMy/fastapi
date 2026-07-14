from sqlmodel import SQLModel , Field, Column ,Relationship
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from typing import Optional , TYPE_CHECKING ,List

class Book(SQLModel,table=True):
    __tablename__ = "books"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    name : str
    user_id : Optional[uuid.UUID] = Field( default=None , foreign_key="Users.uid")
    created_at : datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at : datetime = Field(
        sa_column= Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    user : Optional["User"] = Relationship(back_populates="books")
    review : List["Review"] = Relationship(back_populates="book",sa_relationship_kwargs={"lazy":"selectin"})
    def __repr__(self):
        return f"<BOOk {self.name}>"

class User(SQLModel, table=True):
    __tablename__="Users"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email : str
    role : str = Field(sa_column=Column(
        pg.VARCHAR,
        nullable=False,
        server_default="user"
    ))
    is_verified : bool = Field(sa_column= Column(
        pg.BOOLEAN,
        default=False
    ))
    Password_hash : str = Field(
        exclude=True
    )
    created_at : datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default= datetime.now
        )
    )
    updated_at : datetime = Field (
        sa_column=Column(
            pg.TIMESTAMP,
            default= datetime.now
        )
    )
    books : List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})
    review : List["Review"] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})
    def __repr__(self):
        return f"<USER {self.username}>"


class Review(SQLModel,table=True):
    __tablename__ = "reviews"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating : int = Field(ge=0 , le=5)
    description : str
    user_id : uuid.UUID = Field( default=None , foreign_key="Users.uid")
    book_id : uuid.UUID = Field( default=None , foreign_key="books.uid")
    created_at : datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    updated_at : datetime = Field(
        sa_column= Column(
            pg.TIMESTAMP,
            default=datetime.now
        )
    )
    user : Optional["User"] = Relationship(back_populates="review")
    book : Optional["Book"] = Relationship(back_populates="review")
    def __repr__(self):
        return f"<Review on Book {self.book_id} by user {self.user_id}>"