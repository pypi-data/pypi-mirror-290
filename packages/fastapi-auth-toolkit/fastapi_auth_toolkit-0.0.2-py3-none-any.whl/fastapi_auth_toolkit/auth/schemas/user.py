from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr

from fastapi_auth_toolkit.auth.exception.authentication import UnauthorizedUserException


class UserProfileSchema(BaseModel):
    user_id: PydanticObjectId
    username: str


class UserDetailProfileSchema(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    profile: UserProfileSchema

    @classmethod
    async def from_user(cls, user_obj) -> "UserDetailProfileSchema":
        if user_obj is None:
            raise UnauthorizedUserException("User object is required")

        user_profile_obj = await user_obj.get_profile_obj
        user_profile_dict = user_profile_obj.__dict__  # Convert to dictionary

        user_profile = UserProfileSchema(**user_profile_dict)

        return cls(
            id=user_obj.id,
            email=user_obj.email,
            profile=user_profile
        )
