from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.models import User
from core.exceptions import Unauthorized
from core.helpers import jwt_helper

oauth2_scheme = APIKeyHeader(name="Authorization")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from token"""
    user = await jwt_helper.get_user_from_token(token)
    if user is None:
        raise Unauthorized
    return user
