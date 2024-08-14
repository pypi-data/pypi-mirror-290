from functools import lru_cache

from fastapi import FastAPI

from fastapi_auth_toolkit.auth.middlewares import AuthenticationMiddleware


@lru_cache
def init_middlewares(app: FastAPI):
    """
    Initializes middlewares for the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    # Add your custom AuthenticationMiddleware
    app.add_middleware(AuthenticationMiddleware)
