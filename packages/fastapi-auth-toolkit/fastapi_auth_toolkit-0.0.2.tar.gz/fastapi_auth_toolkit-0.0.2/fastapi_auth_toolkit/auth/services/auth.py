from typing import Any

from fastapi import Request
from pydantic import EmailStr

from fastapi_auth_toolkit.app.config import settings
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum
from fastapi_auth_toolkit.auth.config.authentication import BaseAuthentication

# Retrieve the authentication method and auth model from settings
AUTH_METHOD = settings.auth_method
AuthModel = settings.auth_model


class AuthenticationService(BaseAuthentication):
    @staticmethod
    async def initialize_first_data(email: EmailStr = "admin@admin.com", password: str = "admin"):
        # Check if there are existing auth
        existing_users = await AuthModel.find_all().to_list()

        if not existing_users:
            # Create a new user if none exist
            user = await AuthModel.objects.create_user(email=email, password=password)
            return user

        # Return a message or the first existing user
        # You can modify this based on your requirements
        return existing_users[0]

    async def authenticate_user(self, request: Request, email: str, password: str) -> Any:
        """
        Handle the user authentication process.

        Args:
            request: The FastAPI request object.
            email: The email of the user attempting to authenticate.
            password: The password provided by the user.

        Returns:
            Any: The authenticated user object or None if the user is not authenticated.

        Raises:
            ValueError: If an unsupported authentication method is configured.
        """
        user_obj = await self._authenticate_user(email=email, password=password)

        # Handle authentication based on the configured method
        if user_obj is not None:
            if AUTH_METHOD == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.COOKIES.name_key:
                await self._cookies_authentication(request, user_obj)
            elif AUTH_METHOD == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.SESSION.name_key:
                await self._session_authentication(request, user_obj)
            elif AUTH_METHOD == FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.JWT.name_key:
                await self._jwt_authentication(request, user_obj)
            else:
                raise ValueError("Unsupported authentication method.")

        return user_obj
