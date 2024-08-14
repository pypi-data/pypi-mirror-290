from fastapi import status

from fastapi_auth_toolkit.app.exception import BaseHTTPException
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum


class InvalidTokenException(BaseHTTPException):
    response_code = FastapiAuthEnum.EXCEPTIONS.AUTHENTICATION.TOKEN_NOT_VALID.response_key
    message = FastapiAuthEnum.EXCEPTIONS.AUTHENTICATION.NOT_AUTHENTICATED.value
    status_code = status.HTTP_401_UNAUTHORIZED
