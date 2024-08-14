from fastapi_auth_toolkit.app.utils.enums.auth import AuthExceptionEnum, AuthenticationMethodTypeEnum
from fastapi_auth_toolkit.app.utils.enums.database import DatabaseExceptionEnum
from fastapi_auth_toolkit.app.utils.enums.response import ExceptionTypeEnum


class ExceptionsType:
    AUTHENTICATION = AuthExceptionEnum
    DATABASE = DatabaseExceptionEnum
    RESPONSE = ExceptionTypeEnum


class FastapiAuthEnum:
    EXCEPTIONS = ExceptionsType
    AUTHENTICATION_METHOD_TYPE = AuthenticationMethodTypeEnum
