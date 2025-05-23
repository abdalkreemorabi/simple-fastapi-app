from datetime import datetime
from typing import Annotated
from uuid import uuid4

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import UUID4, EmailStr, Field


class User(Document):
    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid4)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(max_length=255)
    password: str = Field(max_length=255)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"

    async def update(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().update(*args, **kwargs)
