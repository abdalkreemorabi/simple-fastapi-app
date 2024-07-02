from datetime import datetime
from typing import Annotated
from uuid import uuid4

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import UUID4, EmailStr, Field

from core.enums import Gender


class Candidate(Document):
    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid4)

    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(max_length=255)
    major: str = Field(max_length=255)
    years_of_experience: int = Field(default=0)
    skills: list = Field(default=[])
    nationality: str = Field(max_length=255)
    city: str = Field(max_length=255)
    salary: int = Field(default=0)
    gender: Gender
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "candidates"

    async def update(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().update(*args, **kwargs)
