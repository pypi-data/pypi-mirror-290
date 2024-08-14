from pydantic import field_validator

from fastapi_auth_toolkit.auth.models.base import AuthBaseModel


class AuthModel(AuthBaseModel):

    @property
    async def get_profile_obj(self):
        from fastapi_auth_toolkit.auth.models.profile import UserProfileModel

        profile_obj = await UserProfileModel.objects.get_profile_by_user_id(self.id)
        if profile_obj:
            return profile_obj
        new_profile_obj = await UserProfileModel.objects.create(id=self.id, email=self.email)
        if new_profile_obj:
            return new_profile_obj
        return None

    @field_validator('password', mode='before')
    def validate_password(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError('Password must be at least 3 characters long')
        return v
