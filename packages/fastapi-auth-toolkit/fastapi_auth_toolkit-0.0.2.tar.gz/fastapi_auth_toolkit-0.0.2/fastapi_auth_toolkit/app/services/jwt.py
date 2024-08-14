from datetime import datetime
from typing import Dict

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt
from fastapi_auth_toolkit.app.config import settings

# Extract JWT settings
JWT_SECRET_KEY = settings.jwt.secret_key
JWT_ALGORITHM = settings.jwt.algorithm
ACCESS_TOKEN_LIFETIME = settings.jwt.access_token_lifetime
REFRESH_TOKEN_LIFETIME = settings.jwt.refresh_token_lifetime
USER_ID_FIELD = settings.jwt.user_id_field
AUTH_HEADER_TYPES = settings.jwt.auth_header_types
AUTH_HEADER_NAME = settings.jwt.auth_header_name


class JWTServices(HTTPBearer):
    def __init__(self):
        super().__init__()

    @staticmethod
    async def create_access_token(user_id: str) -> str:
        """
        Creates an access token with a specific user ID and expiration time.

        Args:
            user_id (str): The user ID to include in the token.

        Returns:
            str: The encoded JWT access token.
        """
        expire_time = datetime.utcnow() + ACCESS_TOKEN_LIFETIME
        data_payload = {
            USER_ID_FIELD: user_id,
            "type_token": "access",
            "exp": expire_time
        }
        return jwt.encode(data_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    async def create_refresh_token(user_id: str) -> str:
        """
        Creates a refresh token with a specific user ID and expiration time.

        Args:
            user_id (str): The user ID to include in the token.

        Returns:
            str: The encoded JWT refresh token.
        """
        expire_time = datetime.utcnow() + REFRESH_TOKEN_LIFETIME
        data_payload = {
            USER_ID_FIELD: user_id,
            "type_token": "refresh",
            "exp": expire_time
        }
        return jwt.encode(data_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    async def decode_token(token: str) -> Dict:
        """
        Decodes a JWT token and verifies its validity.

        Args:
            token (str): The JWT token to decode.

        Returns:
            Dict: The decoded token payload.

        Raises:
            HTTPException: If the token is expired or invalid.
        """
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": f"{AUTH_HEADER_TYPES} {AUTH_HEADER_NAME}"}
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": f"{AUTH_HEADER_TYPES} {AUTH_HEADER_NAME}"}
            )

    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials) -> str:
        """
        Verifies the JWT token and extracts the user ID.

        Args:
            credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials containing the JWT token.

        Returns:
            str: The user ID extracted from the token.

        Raises:
            HTTPException: If the token is invalid or user ID is missing.
        """
        token = credentials.credentials
        try:
            payload = await JWTServices.decode_token(token)
            user_id = payload.get(USER_ID_FIELD)
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User ID not found in token"
                )
            return user_id
        except HTTPException as exc:
            raise exc  # Re-raise known exceptions
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": f"{AUTH_HEADER_TYPES} {AUTH_HEADER_NAME}"}
            )
