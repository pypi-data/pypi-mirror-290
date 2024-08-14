import secrets
from datetime import timedelta

from pydantic import BaseModel


class JWTSettings(BaseModel):
    """
    Configuration settings for JSON Web Tokens (JWT).

    Attributes:
        access_token_lifetime (timedelta): The duration for which the access token is valid.
                                           Default is 60 minutes.
        refresh_token_lifetime (timedelta): The duration for which the refresh token is valid.
                                            Default is 1 day.
        update_last_login (bool): Flag indicating whether to update the user's last login time
                                  when a new token is issued. Default is False.
        algorithm (str): The algorithm used for signing the JWT. Default is 'HS256'.
        auth_header_types (str): The type of authorization header to use (e.g., 'Bearer').
                                 Default is 'Bearer'.
        auth_header_name (str): The name of the HTTP header used for authorization. Default is 'Authorization'.
        user_id_field (str): The field name in the JWT payload that represents the user ID. Default is 'user_id'.
        secret_key (str): The secret key used for encoding and decoding the JWT.
                          Generated automatically by `secrets.token_urlsafe` if not provided.

    """
    access_token_lifetime: timedelta = timedelta(minutes=60)  # Validity duration of access tokens
    refresh_token_lifetime: timedelta = timedelta(days=1)  # Validity duration of refresh tokens
    update_last_login: bool = False  # Whether to update the last login time on token issuance
    algorithm: str = "HS256"  # JWT signing algorithm
    auth_header_types: str = "Bearer"  # Type of authorization header (e.g., 'Bearer')
    auth_header_name: str = "Authorization"  # Name of the HTTP authorization header
    user_id_field: str = "user_id"  # Key in JWT payload for user ID

    secret_key: str = secrets.token_urlsafe(32)  # Secret key for encoding/decoding JWT

    class Config:
        """
        Configuration for Pydantic model behavior.
        """
        extra = "ignore"  # Ignore any extra fields that are not defined in the model
