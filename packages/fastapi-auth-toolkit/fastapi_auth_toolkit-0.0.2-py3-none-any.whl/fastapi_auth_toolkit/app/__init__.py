from typing import Optional, Dict, Type, List, Any

from beanie import Document
from fastapi import FastAPI

from fastapi_auth_toolkit.app.config import settings
from fastapi_auth_toolkit.app.settings.jwt import JWTSettings
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum
from fastapi_auth_toolkit.auth.models import AuthModel, UserProfileModel
from fastapi_auth_toolkit.auth.routers import auth_router


class BaseFastapiAuthToolkitConfig:
    def __init__(self,
                 app: FastAPI,
                 document_models: Optional[List[Type[Document]]],
                 auth_method: Optional[str] = None,
                 jwt_settings: Optional[Dict[str, Any]] = None,
                 ):
        """
        Initialize FastAPI application with Beanie and JWT settings.

        :param app: The FastAPI application instance.
        :param document_models: A list of Beanie document model classes to be used.
        :param auth_method: Optional authentication method.
        :param jwt_settings: Optional dictionary of JWT settings.
        :raises ValueError: If `app` or `document_models` is not provided.
        """
        if not app:
            raise ValueError("FastAPI app instance must be provided.")

        # Validate the auth_method
        if auth_method is not None:
            valid_auth_methods = {e.name_key for e in FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE}
            if auth_method not in valid_auth_methods:
                raise ValueError(f"auth_method must be one of {valid_auth_methods}")

            settings.auth_method = auth_method

        # Apply JWT settings if provided
        if jwt_settings:
            try:
                updated_jwt_settings = JWTSettings(**jwt_settings)
                settings.jwt = updated_jwt_settings
            except TypeError as e:
                raise ValueError("Invalid JWT settings provided. Ensure all required fields are present.") from e

        # Ensure default document models are included
        if AuthModel not in document_models:
            document_models.append(AuthModel)
        if UserProfileModel not in document_models:
            document_models.append(UserProfileModel)

        app.include_router(auth_router)
