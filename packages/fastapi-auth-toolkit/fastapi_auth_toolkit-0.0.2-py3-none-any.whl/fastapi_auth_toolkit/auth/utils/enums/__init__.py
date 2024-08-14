from fastapi_auth_toolkit.auth.utils.enums.account import AuthExceptionEnum, PasswordExceptionEnum, UsernameExceptionEnum
from fastapi_auth_toolkit.auth.utils.enums.choices import UserActionTypeEnum


class ExceptionsType:
    AUTHENTICATION = AuthExceptionEnum
    PASSWORD = PasswordExceptionEnum
    USERNAME = UsernameExceptionEnum


class UserChoiceType:
    USER_ACTIONS = UserActionTypeEnum


class AuthEnum:
    EXCEPTIONS = ExceptionsType
    CHOICE = UserChoiceType
