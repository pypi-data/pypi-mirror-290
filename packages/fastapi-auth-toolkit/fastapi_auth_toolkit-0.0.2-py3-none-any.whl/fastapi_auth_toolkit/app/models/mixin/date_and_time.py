from datetime import datetime

from beanie import after_event, Replace
from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow,
                                 description="Timestamp when the document was created.")
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 description="Timestamp when the document was last updated.")

    @after_event(Replace)
    def update_timestamps(self):
        """Update the `updated_at` field with the current timestamp."""
        self.updated_at = datetime.utcnow()
