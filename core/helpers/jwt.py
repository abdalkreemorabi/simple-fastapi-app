import uuid
from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt

from app.models import Candidate, User
from core.exceptions import (
    CandidateNotFound,
    InvalidTokenPayload,
    Unauthorized,
    UserNotFound,
)
from core.settings import AppSettings, get_settings


class JWTHelper:
    """
    Helper class for JWT operations
    """

    def decode_token(self, token):
        """
        Decode token
        :param token:
        :return: token payload
        """
        return jwt.decode(
            token,
            get_settings(AppSettings).SECRET_KEY,
            algorithms=[get_settings(AppSettings).ALGORITHM],
        )

    def create_access_token(self, user: User):
        """
        Create access token
        :param user:
        """
        return self._genereate_token(user)

    def _genereate_token(
        self,
        user: User | Candidate,
        expires_delta: timedelta = None,
    ):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=get_settings(AppSettings).ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {
            "uuid": user.uuid,
            "email": user.email,
            "exp": int(expire.timestamp()),
        }
        to_encode = jsonable_encoder(to_encode)
        encoded_jwt = jwt.encode(
            to_encode,
            get_settings(AppSettings).SECRET_KEY,
            algorithm=get_settings(AppSettings).ALGORITHM,
        )
        return encoded_jwt

    async def get_user_from_token(self, token: str):
        """
        Get user from token
        :param token:
        :return: User | Candidate

        this method will raise AuthorizationException if token is invalid or user not found
        """
        try:
            payload = self.decode_token(token)
            user_uuid: str = payload.get("uuid")

            if user_uuid is None:
                raise InvalidTokenPayload

            obj = await User.find_one(User.uuid == uuid.UUID(user_uuid))
            return obj
        except (InvalidTokenPayload, UserNotFound, CandidateNotFound) as e:
            raise e
        except JWTError as e:
            raise Unauthorized

    def get_expiration_time(self):
        """
        Get expiration time
        :return: expiration time
        """
        return datetime.utcnow() + timedelta(
            minutes=get_settings(AppSettings).ACCESS_TOKEN_EXPIRE_MINUTES
        )


jwt_helper = JWTHelper()
