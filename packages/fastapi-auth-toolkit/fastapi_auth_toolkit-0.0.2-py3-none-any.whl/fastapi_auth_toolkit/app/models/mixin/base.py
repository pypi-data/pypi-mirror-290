from typing import Annotated

from bson import ObjectId
from pydantic import Field, ConfigDict

from fastapi_auth_toolkit.app.models.mixin.date_and_time import DateTimeModelMixin


class CustomBaseModelMixin(DateTimeModelMixin):
    id: Annotated[ObjectId, Field(default_factory=ObjectId, alias='_id')]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    @classmethod
    def set_manager(cls, manager):
        cls.objects = manager(cls)
