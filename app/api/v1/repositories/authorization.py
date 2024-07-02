from app.api.v1.serializers import authorization as authorization_serializers
from app.models import User
from core.exceptions import InvalidCredentials, UserNotFound
from core.helpers import hash_helper, jwt_helper


async def _login(
        payload: authorization_serializers.LoginFormSerializer, model: User
):
    user = await model.find(model.email == str(payload.email)).first_or_none()

    if not user:
        raise UserNotFound

    if not hash_helper.verify_password(payload.password, user.password):
        raise InvalidCredentials

    return {
        "access_token": jwt_helper.create_access_token(user),
        "exp": jwt_helper.get_expiration_time(),
    }


async def user_login(payload: authorization_serializers.LoginFormSerializer):
    return await _login(payload, User)
