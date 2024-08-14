from typing import Type

from bson import ObjectId


class UserProfileManager:
    def __init__(self, model: Type):
        self.model = model

    async def create(self, user_id: ObjectId, email: str):
        if not user_id:
            raise ValueError('User ID is required')

        if not email:
            raise ValueError('Email is required')

        profile = self.model(
            user_id=user_id,
            email=email,
            username=email.split('@')[0],  # Setting a default username based on email
        )
        new_user_profile_obj = await profile.save()

        return new_user_profile_obj

    async def get_profile_by_user_id(self, user_id: ObjectId):
        user_profile_obj = await self.model.find_one({"user_id": user_id})
        if user_profile_obj:
            return user_profile_obj
        return None

