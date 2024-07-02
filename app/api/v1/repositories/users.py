from app.api.v1.serializers import users as users_serializers
from app.models import User
from core.exceptions import UserEmailAlreadyExists
from core.helpers import hash_helper


async def create_user(payload: users_serializers.RegisterUserSerializer) -> User:
    """
    Async function to create user.

    :param payload: RegisterUserSerializer
    :return: user
    """
    data = payload.model_dump()

    user = await User.find({"email": data["email"]}).first_or_none()
    if user:
        raise UserEmailAlreadyExists

    data["password"] = hash_helper.get_password_hash(data["password"])
    user = await User(**data).insert()

    return users_serializers.User(**user.model_dump())
