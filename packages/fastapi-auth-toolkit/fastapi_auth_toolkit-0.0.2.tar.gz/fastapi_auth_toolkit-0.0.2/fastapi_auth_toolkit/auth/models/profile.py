from typing import Optional

from beanie import Document
from bson import ObjectId
from pydantic import EmailStr, Field, HttpUrl
from pymongo import IndexModel, ASCENDING

from fastapi_auth_toolkit.app.models.mixin.base import CustomBaseModelMixin


class UserProfileModel(Document, CustomBaseModelMixin):
    user_id: ObjectId = Field(..., description="User ID")
    username: Optional[str] = Field(..., min_length=3, max_length=64, description="Password")
    email: EmailStr = Field(..., description="Email address")
    bio: Optional[str] = Field(None, description="User bio")
    profile_picture: Optional[HttpUrl] = Field(None, description="URL of the profile picture")

    class Settings:
        name = "user_profiles"
        indexes = [
            IndexModel([("user_id", ASCENDING)], unique=True),
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("username", ASCENDING)], unique=True),
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "605c72ef3f1c4d47f431d0e8",
                "username": "ankajgupta",
                "email": "john_doe@example.com",
                "bio": "Software developer with a passion for open-source projects.",
                "profile_picture": "http://example.com/profile.jpg",
                "joined_at": "2024-07-27T00:00:00Z"
            }
        }
