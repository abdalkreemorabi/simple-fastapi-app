from fastapi import APIRouter, status

from app.api.v1.serializers import users as users_serializers
from app.api.v1.repositories import users as users_repo
from core.constants import ResponseMessages
from core.utils import response_handler

router = APIRouter()


@router.post("", response_model=users_serializers.UserOut)
async def create_user(payload: users_serializers.RegisterUserSerializer):
    """
    API endpoint to create new user.
    """

    return response_handler(
        data=await users_repo.create_user(payload),
        status=status.HTTP_201_CREATED,
        message=ResponseMessages.Retrieved,
    )
