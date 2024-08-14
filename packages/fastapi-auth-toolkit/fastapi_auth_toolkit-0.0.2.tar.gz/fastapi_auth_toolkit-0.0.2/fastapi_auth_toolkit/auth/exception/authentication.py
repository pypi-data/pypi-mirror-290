from fastapi import status

from fastapi_auth_toolkit.app.exception import BaseHTTPException
from fastapi_auth_toolkit.auth.utils.enums import AuthEnum


class AuthenticationFailedException(BaseHTTPException):
    """
    Exception raised when authentication fails.
    """
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.AUTHENTICATION_FAILED.response_key
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.AUTHENTICATION_FAILED.value


class NotAuthenticatedException(BaseHTTPException):
    """
    Exception raised when a user is not authenticated.
    """
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.NOT_AUTHENTICATED.response_key
    status_code = status.HTTP_401_UNAUTHORIZED
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.NOT_AUTHENTICATED.value


class AlreadyAuthenticatedException(BaseHTTPException):
    """
    Exception raised when a user is already authenticated.
    """
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.ALREADY_AUTHENTICATED.response_key
    status_code = status.HTTP_401_UNAUTHORIZED
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.ALREADY_AUTHENTICATED.value


class UnauthorizedUserException(BaseHTTPException):
    """
    Exception raised when a user is authenticated but not authorized to perform a specific action.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.UNAUTHORIZED_USER.response_key
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.UNAUTHORIZED_USER.value


class AccountNotActiveException(BaseHTTPException):
    """
    Exception raised when a user is not active.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_ACTIVE.response_key
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_ACTIVE.value


class AccountNotExistsException(BaseHTTPException):
    """
     Exception raised when a user with the provided credentials does not exist.
    """
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_EXIST.response_key
    status_code = status.HTTP_404_NOT_FOUND
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.ACCOUNT_NOT_EXIST.value


class AccountAlreadyExistsException(BaseHTTPException):
    """
     Exception raised when a user with the provided credentials already exists.
    """
    response_code = AuthEnum.EXCEPTIONS.AUTHENTICATION.PERMISSION_DENIED.response_key
    message = AuthEnum.EXCEPTIONS.AUTHENTICATION.PERMISSION_DENIED.value
    status_code = status.HTTP_409_CONFLICT


class PasswordInvalidException(BaseHTTPException):
    """
     Exception raised when a user with the provided password does not verify.
    """
    response_code = AuthEnum.EXCEPTIONS.PASSWORD.PASSWORD_NOT_VALID.response_key
    message = AuthEnum.EXCEPTIONS.PASSWORD.PASSWORD_NOT_VALID.value
