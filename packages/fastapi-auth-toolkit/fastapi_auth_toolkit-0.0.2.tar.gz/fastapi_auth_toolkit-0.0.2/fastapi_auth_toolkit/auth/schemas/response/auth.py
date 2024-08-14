from typing import Optional

from pydantic import Field, BaseModel

from fastapi_auth_toolkit.app.config import settings
from fastapi_auth_toolkit.app.exception.permissions import PermissionDeniedException
from fastapi_auth_toolkit.app.schemas.jwt import AuthTokenSchema
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum
from fastapi_auth_toolkit.auth.schemas.user import UserDetailProfileSchema
from fastapi_auth_toolkit.auth.utils.enums import AuthEnum


class UserRegisterSuccessSchema(BaseModel):
    response_code: str = Field(default=AuthEnum.CHOICE.USER_ACTIONS.ACCOUNT_CREATED.response_key)
    message: str = Field(default=AuthEnum.CHOICE.USER_ACTIONS.ACCOUNT_CREATED.value)


class UserLoginSuccessSchema(BaseModel):
    response_code: str = Field(default=AuthEnum.CHOICE.USER_ACTIONS.LOGIN_SUCCESS.response_key)
    message: str = Field(default=AuthEnum.CHOICE.USER_ACTIONS.LOGIN_SUCCESS.value)
    token: Optional[AuthTokenSchema | None] = None
    user: UserDetailProfileSchema

    class Config:
        json_schema_extra = {
            "examples": [{
                "jwt_login": {
                    "message": "User logged in successfully",
                    "token": {
                        "access_token": "example_access_token",
                        "refresh_token": "example_refresh_token",
                        "token_type": "bearer"
                    },
                    "user": {
                        "id": "example_user_id",
                        "email": "example_email",
                        "profile": {
                            "user_id": "example_user_id",
                            "username": "example_username",
                        }
                    }
                },
                "session_login": {
                    "message": "User logged in successfully",
                    "user": {
                        "id": "example_user_id",
                        "email": "example_email",
                        "profile": {
                            "user_id": "example_user_id",
                            "username": "example_username",
                        }
                    }
                },
                "cookies_login": {
                    "message": "User logged in successfully",
                    "user": {
                        "id": "example_user_id",
                        "email": "example_email",
                        "profile": {
                            "user_id": "example_user_id",
                            "username": "example_username",
                        }
                    }
                }
            }]
        }

    @classmethod
    async def from_user_obj(cls, user_obj) -> "UserLoginSuccessSchema":
        if user_obj is None:
            raise PermissionDeniedException("User object is required")

        # Initialize variables
        token = None
        user_details = await UserDetailProfileSchema.from_user(user_obj)

        # Check authentication method and generate token if required
        if settings.auth_method == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.JWT.name_key:
            token = await AuthTokenSchema.get_tokens(str(user_obj.id))

        return cls(token=token, user=user_details)
