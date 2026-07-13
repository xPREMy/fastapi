from sqlmodel import SQLModel , Field, Column ,Relationship
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from typing import Optional , TYPE_CHECKING ,List
if TYPE_CHECKING:
    from src.books.models import Book

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

    def __repr__(self):
        return f"<USER {self.username}>"
