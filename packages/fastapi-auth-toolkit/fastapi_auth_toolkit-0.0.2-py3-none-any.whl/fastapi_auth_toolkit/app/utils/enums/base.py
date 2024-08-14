from enum import Enum


# Define a base class for custom string-based enumerations
class BaseCustomEnum(str, Enum):

    def __str__(self):
        # Override the string representation to return the value in title case
        return self.value.title()

    @property
    def name_key(self):
        # Create a custom choices key by converting the name to lowercase
        return self.name.lower()

    @property
    def response_key(self):
        # Create a custom response key by replacing single underscores with double underscores and converting to lowercase
        return self.name.lower().replace("_", "__")

