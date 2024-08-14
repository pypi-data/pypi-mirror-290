from bson import ObjectId
from fastapi import Request, Response


async def get_response(request: Request) -> Response:
    return Response()


def str_to_objectid(id_str: str) -> ObjectId:
    """
    Convert a string to an ObjectId.

    Args:
        id_str (str): The string representation of the ObjectId.

    Returns:
        ObjectId: The converted ObjectId.

    Raises:
        ValueError: If the string is not a valid ObjectId.
    """
    try:
        return ObjectId(id_str)
    except Exception as e:
        raise ValueError(f"Invalid ObjectId string: {e}")


class classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self
