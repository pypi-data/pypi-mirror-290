from pydantic import BaseModel

from fastapi_auth_toolkit.app.config import settings
from fastapi_auth_toolkit.app.exception.permissions import PermissionDeniedException
from fastapi_auth_toolkit.app.services.jwt import JWTServices


# Define a schema for authentication tokens using Pydantic's BaseModel
class AuthTokenSchema(BaseModel):
    # Define the attributes for the schema with types
    access_token: str
    refresh_token: str
    token_type: str = settings.jwt.auth_header_types

    # Configure the schema to include an example in the generated JSON schema
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "example_access_token",
                "refresh_token": "example_refresh_token",
                "token_type": settings.jwt.auth_header_types
            }
        }

    # Define a class method to create an AuthTokenSchema instance from a user ID
    @classmethod
    async def get_tokens(cls, user_id) -> "AuthTokenSchema":
        # Raise an exception if the user ID is None
        if user_id is None:
            raise PermissionDeniedException

        # Generate access and refresh tokens using the JWT services
        access_token = await JWTServices.create_access_token(user_id)
        refresh_token = await JWTServices.create_refresh_token(user_id)

        # Return an instance of AuthTokenSchema with the generated tokens
        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
        )
