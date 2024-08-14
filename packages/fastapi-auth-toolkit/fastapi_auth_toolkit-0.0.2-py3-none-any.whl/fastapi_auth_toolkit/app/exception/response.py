from fastapi_auth_toolkit.app.exception import BaseHTTPException
from fastapi import status

from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum


class NotFoundException(BaseHTTPException):
    """
    Exception raised when a user does not have the necessary permissions.
    """
    response_code = FastapiAuthEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.response_key
    status_code = status.HTTP_403_FORBIDDEN
    message = FastapiAuthEnum.EXCEPTIONS.RESPONSE.NOT_FOUND.value
