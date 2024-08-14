from typing import Optional

from fastapi import Request
from jwt import InvalidTokenError, ExpiredSignatureError

from fastapi_auth_toolkit.app.config import settings
from fastapi_auth_toolkit.app.exception.database import DataFetchingException
from fastapi_auth_toolkit.app.services.jwt import JWTServices
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum
from fastapi_auth_toolkit.auth.exception.authentication import UnauthorizedUserException, AlreadyAuthenticatedException
from fastapi_auth_toolkit.auth.services import AuthenticationService

# Retrieve the authentication method from settings
AUTHENTICATION_METHOD = settings.auth_method


async def get_auth_model():
    """
    Returns the AuthModel class as defined in the settings.

    Returns:
        Type[AuthModel]: The AuthModel class used for user operations.
    """
    return settings.auth_model


async def get_current_user(request: Request) -> Optional[dict]:
    """
    Retrieve the user associated with the request based on the authentication method specified in settings.

    Args:
        request (Request): The FastAPI request object containing session, cookies, or headers.

    Returns:
        Optional[dict]: User data if authenticated, otherwise None.

    Raises:
        UnauthorizedUserException: If the JWT token is invalid or expired.
        DataFetchingException: If there's an error fetching user data from the database.
    """
    AuthModel = settings.auth_model
    user_id = None
    try:

        # Handle different authentication methods
        if AUTHENTICATION_METHOD == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.SESSION.name_key:
            # Get user ID from session
            user_id = request.session.get('user_id')
        elif AUTHENTICATION_METHOD == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.COOKIES.name_key:
            # Get user ID from cookies
            user_id = request.cookies.get('user_id')
        elif AUTHENTICATION_METHOD == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.JWT.name_key:
            # Get JWT token from request headers
            token = request.headers.get(settings.jwt.auth_header_name)
            if token and token.startswith(f"{settings.jwt.auth_header_types} "):
                # Remove the prefix (e.g., 'Bearer ')
                token = token[len(settings.jwt.auth_header_types) + 1:]
                try:
                    # Validate and decode JWT token
                    payload = await JWTServices.decode_token(token)
                    user_id = payload.get(settings.jwt.user_id_field)
                except (ExpiredSignatureError, InvalidTokenError) as e:
                    # Raise custom exception if token is invalid or expired
                    raise UnauthorizedUserException(detail=str(e),
                        headers={"WWW-Authenticate": f"{settings.jwt.auth_header_types} {settings.jwt.auth_header_name}"})

        # Fetch user from database if user_id is obtained
        if user_id:
            try:
                user = await AuthModel.objects.get_object_by_id(user_id)  # Assuming this is an async method
            except Exception as e:
                # Raise custom exception for errors during database operations
                raise DataFetchingException(message="Error fetching user from database", detail=str(e), )
            return user

    except Exception as e:
        print(f"Error in get_current_user: {str(e)}")

    return None


async def authenticate(request: Request, email: str, password: str) -> bool:
    """
    Authenticate a user by email and password.

    :param email: The email of the user.
    :param password: The password of the user.
    :return: The authenticated user object if successful.
    :raises AccountNotExistsException: If the user does not exist or the password is incorrect.
    """
    current_user = await get_current_user(request)

    if current_user is not None:
        raise AlreadyAuthenticatedException

    # Check if email is provided
    if not email:
        raise ValueError('Email should be provided.')

    # Check if password is provided
    if not password:
        raise ValueError('Password should not be None or empty.')

    #
    user_obj = await AuthenticationService.authenticate_user(request=request, email=email, password=password)

    return user_obj
