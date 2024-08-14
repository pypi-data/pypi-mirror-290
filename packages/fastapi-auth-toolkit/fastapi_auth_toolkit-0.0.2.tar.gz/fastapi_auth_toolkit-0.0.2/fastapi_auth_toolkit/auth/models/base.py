from typing import Optional

from beanie import Document
from pydantic import Field, EmailStr
from pymongo import IndexModel, ASCENDING

from fastapi_auth_toolkit.app.models.mixin.base import CustomBaseModelMixin
from fastapi_auth_toolkit.app.services.password import PasswordService


class AuthBaseModel(Document, CustomBaseModelMixin):
    email: EmailStr = Field(..., description="Email address")
    password: Optional[str] = Field(..., min_length=3, max_length=64, description="Password")
    is_active: bool = Field(default_factory=lambda: False, description="Whether the resource is still actively maintained.")

    class Settings:
        name = "all_users"
        validate_on_save = True
        indexes = [
            IndexModel([("email", ASCENDING)], unique=True)
        ]

    def set_password(self, raw_password: str):
        self.password = PasswordService.hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return PasswordService.verify_password(raw_password, self.password)
