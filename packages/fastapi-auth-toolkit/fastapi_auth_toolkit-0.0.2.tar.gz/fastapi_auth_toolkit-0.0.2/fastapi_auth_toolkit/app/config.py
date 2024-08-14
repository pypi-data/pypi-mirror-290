from typing import Type, ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings

from fastapi_auth_toolkit.app.settings import JWTSettings, CookieSettings, SessionSettings
from fastapi_auth_toolkit.app.utils.enums import FastapiAuthEnum
from fastapi_auth_toolkit.auth.models import AuthModel


class Settings(BaseSettings):
    auth_model: ClassVar[Type[AuthModel]] = AuthModel

    # authentication method based on environment variable or configuration
    auth_method: str = FastapiAuthEnum.AUTHENTICATION_METHOD_TYPE.SESSION.name_key

    # jwt configuration and credentials settings
    jwt: JWTSettings = Field(default_factory=JWTSettings)

    # cookie configuration and credentials settings
    cookie: CookieSettings = Field(default_factory=CookieSettings)

    # session configuration and credentials settings
    session: SessionSettings = Field(default_factory=SessionSettings)


settings = Settings()
