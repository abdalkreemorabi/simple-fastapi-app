from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from beanie import PydanticObjectId
from fastapi import Query
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from core.constants import CANDIDATE_SUPPORTED_FILTERS
from core.enums import Gender, Order
from core.utils import ResponseModel

from .base import BaseUserSerializer


class Candidates(BaseModel):
    """
    Candidates pydantic model to be used in query projection
    """

    _id: PydanticObjectId
    uuid: UUID
    first_name: str
    last_name: str
    email: str
    major: str
    years_of_experience: int
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: Gender
    created_at: datetime
    updated_at: datetime


class RegisterCandidateSerializer(BaseUserSerializer):
    """Register Candidate Serializer"""

    major: str
    years_of_experience: int
    skills: List[str]
    nationality: str
    city: str
    salary: int
    gender: Gender


class UpdateCandidateSerializer(BaseModel):
    """Update Candidate Serializer"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    major: Optional[str] = None
    years_of_experience: Optional[int] = None
    skills: Optional[List[str]] = None
    nationality: Optional[str] = None
    city: Optional[str] = None
    salary: Optional[int] = None
    gender: Optional[Gender] = None

    @model_validator(mode="after")
    def validate_fields(self):
        """
        Validate fields to be updated
        if no fields to update raise ValueError
        """

        data = self.model_dump(exclude_none=True)
        if not data:
            raise ValueError("No fields to update")

        return self


class CandidatesSearchSerializer(BaseModel):
    """
    Candidates search serializer
    sort: sort field it can be one of candidate fields
    """

    page: int = Query(1, ge=1)
    page_size: int = Query(10, ge=1, le=100)

    sort: Optional[str] = Query(None)
    order: Optional[Order] = Query(default=Order.ASC)
    first_name: Optional[str] = Query(None)
    last_name: Optional[str] = Query(None)
    email: Optional[EmailStr] = Query(None)
    major: Optional[str] = Query(None)
    years_of_experience: Optional[int] = Query(None)
    skills: Optional[str] = Query(None)
    nationality: Optional[str] = Query(None)
    city: Optional[str] = Query(None)
    salary: Optional[int] = Query(None)
    gender: Optional[Gender] = Query(None)

    @field_validator("sort")
    @classmethod
    def validate_sort(cls, v):
        """
        Validate sort field to be one of candidate fields
        """
        if v and v not in CANDIDATE_SUPPORTED_FILTERS:
            raise ValueError("Invalid sort field")
        return v


class CandidateOut(ResponseModel):
    """Candidate Out Serializer"""

    data: Candidates


class SearchCandidatesOut(ResponseModel):
    """Search Candidates Out Serializer"""

    data: List[Candidates]


class GenerateReportOut(ResponseModel):
    """
    Generate Report Out Serializer
    """

    data: Any


class DeleteCandidateOut(ResponseModel):
    """
    Delete Candidate Out Serializer
    """

    data: None = None
