from typing import Type

from fastapi_auth_toolkit.app.utils.functions import str_to_objectid


class BaseModelManager:
    def __init__(self, model: Type):
        self.model = model

    async def get_object_by_id(self, id_str: int | str):
        existing_user = await self.model.find_one({"_id": str_to_objectid(id_str)})
        if existing_user:
            return existing_user
        return None
