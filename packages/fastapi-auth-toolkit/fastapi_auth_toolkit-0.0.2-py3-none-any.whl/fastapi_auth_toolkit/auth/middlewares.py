from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from fastapi_auth_toolkit.auth.helpers.authentication import get_current_user


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Middleware to authenticate user and attach user information to the request.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): A function to process the request and return a response.

        Returns:
            Response: The response object returned from processing the request.
        """
        # Initialize user to None
        request.state.user = None

        # Fetch the current user based on the authentication method
        user_obj = await get_current_user(request)
        if user_obj:
            request.state.user = user_obj

        # Proceed with the request
        response = await call_next(request)
        return response
