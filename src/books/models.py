from sqlmodel import SQLModel, Field, Column ,Relationship
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid
from typing import Optional , TYPE_CHECKING
if TYPE_CHECKING:
    from src.auth.models import User

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

    def __repr__(self):
        return f"<BOOk {self.name}>"