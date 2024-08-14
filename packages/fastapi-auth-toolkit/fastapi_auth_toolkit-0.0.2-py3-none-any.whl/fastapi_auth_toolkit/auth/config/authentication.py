from datetime import datetime
from typing import Type

from fastapi import Request

from fastapi_auth_toolkit.app.config import settings
from fastapi_auth_toolkit.app.utils.functions import get_response
from fastapi_auth_toolkit.auth.exception.authentication import (
    AccountNotExistsException,
    PasswordInvalidException,
    AccountNotActiveException
)

# Retrieve the auth model from settings
AuthModel = settings.auth_model


class BaseAuthentication:
    def _user_can_authenticate(self, auth_obj) -> bool:
        """
        Check if the user can be authenticated based on their active status.
        Users with `is_active=False` are rejected unless the attribute is missing.

        Args:
            auth_obj: The user object to check.

        Returns:
            bool: True if the user is active or the attribute is missing, False otherwise.
        """
        return getattr(auth_obj, "is_active", True)

    async def _authenticate_user(self, email: str, password: str) -> Type[AuthModel]:
        """
        Authenticate a user based on email and password.

        Args:
            email: The email of the user attempting to authenticate.
            password: The password provided by the user.

        Returns:
            AuthModel: The authenticated user object.

        Raises:
            AccountNotExistsException: If the user with the given email does not exist.
            PasswordInvalidException: If the provided password is incorrect.
            AccountNotActiveException: If the user account is not active.
        """
        # Fetch the user by email
        user_obj = await AuthModel.objects.get_user_by_email(email)

        # Check if the user exists
        if not user_obj:
            raise AccountNotExistsException(detail="User with this email does not exist.")

        # Validate the password
        if not user_obj.verify_password(password):
            raise PasswordInvalidException(detail="Incorrect password provided.")

        # Check if the user can be authenticated
        if not self._user_can_authenticate(user_obj):
            raise AccountNotActiveException

        return user_obj

    async def _session_authentication(self, request: Request, user_obj: AuthModel) -> None:
        """
        Handle session-based authentication by setting a session for the user.

        Args:
            request: The FastAPI request object.
            user_obj: The authenticated user object.
        """
        # Example: Store the user ID in the session
        request.session['user_id'] = str(user_obj.id)

    async def _cookies_authentication(self, request: Request, user_obj: AuthModel) -> None:
        """
        Handle cookie-based authentication by setting a cookie for the user.

        Args:
            request: The FastAPI request object.
            user_obj: The authenticated user object.
        """
        # Define response object to set cookies on.
        response = await get_response(request)

        # Define cookie settings
        cookie_value = str(user_obj.id)  # Typically this could be a session ID or a token
        expires = datetime.utcnow() + settings.cookie.expires_time  # Set the cookie to expire based on the configured time

        # Set the cookie on the response
        response.set_cookie(
            key=settings.cookie.cookie_name,
            value=cookie_value,
            expires=expires,
            httponly=settings.cookie.httponly,  # Use settings for HttpOnly attribute
            secure=settings.cookie.cookie_secure,  # Use settings for secure attribute
            samesite=settings.cookie.samesite  # Use settings for SameSite attribute
        )

    async def _jwt_authentication(self, request: Request, user_obj: AuthModel) -> None:
        """
        Handle JWT-based authentication by generating and setting a JWT for the user.

        Args:
            request: The FastAPI request object.
            user_obj: The authenticated user object.
        """
        # Implement JWT-based authentication logic
        # Example: Generate JWT token and set it in the response header
        pass
