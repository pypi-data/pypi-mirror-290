from bson import ObjectId

from fastapi_auth_toolkit.auth.models.profile import UserProfileModel


async def create_user_profile_event(user_id: ObjectId, email: str):
    created_user = await UserProfileModel.objects.create(
        user_id=user_id,
        email=email,
    )
    return created_user
