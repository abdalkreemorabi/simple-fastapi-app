from uuid import UUID

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from core.utils import ResponseModel
from .base import BaseUserSerializer


class RegisterUserSerializer(BaseUserSerializer):
    """Register User Serializer"""

    password: str = Field(max_length=255)


class User(BaseModel):
    """
    User pydantic model to be used in query projection
    """

    _id: PydanticObjectId
    uuid: UUID
    first_name: str
    last_name: str
    email: str


class UserOut(ResponseModel):
    """User Out Serializer to be used in response"""

    data: User
