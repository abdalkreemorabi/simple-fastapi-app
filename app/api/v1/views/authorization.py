from fastapi import APIRouter, status
from app.api.v1.serializers import authorization as authorization_serializers
from app.api.v1.repositories import authorization as authorization_repo
from core.constants.responses import ResponseMessages
from core.utils import response_handler

router = APIRouter()


@router.post("/login", response_model=authorization_serializers.LoginOut)
async def user_login(payload: authorization_serializers.LoginFormSerializer):
    """
    API endpoint to login user.
    """
    return response_handler(
        data=await authorization_repo.user_login(payload),
        status=status.HTTP_200_OK,
        message=ResponseMessages.Retrieved,
    )
