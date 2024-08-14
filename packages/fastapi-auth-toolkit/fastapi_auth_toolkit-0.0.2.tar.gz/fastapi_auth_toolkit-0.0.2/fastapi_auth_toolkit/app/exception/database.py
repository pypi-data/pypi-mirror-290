from fastapi import status

from fastapi_auth_toolkit.app.exception import BaseHTTPException
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum


class DataFetchingException(BaseHTTPException):
    """
    Exception raised when a user does not have the necessary permissions.
    """
    response_code = FastapiAuthEnum.EXCEPTIONS.DATABASE.DATA_FETCH_FAILED.response_key
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = FastapiAuthEnum.EXCEPTIONS.DATABASE.DATA_FETCH_FAILED.value
