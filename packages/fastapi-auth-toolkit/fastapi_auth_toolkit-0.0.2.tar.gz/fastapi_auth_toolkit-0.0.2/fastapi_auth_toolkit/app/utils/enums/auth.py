from fastapi_auth_toolkit.app.utils.enums.base import BaseCustomEnum


class AuthenticationMethodTypeEnum(BaseCustomEnum):
    JWT = 'JWT-based authentication'
    SESSION = "Session based authentication"
    COOKIES = "Cookies based authentication"


class AuthExceptionEnum(BaseCustomEnum):
    NOT_AUTHENTICATED = 'Authentication credentials were not provided.'
    PERMISSION_DENIED = 'You do not have permission to perform this action.'
    TOKEN_NOT_VALID = "Token is invalid or expired"
