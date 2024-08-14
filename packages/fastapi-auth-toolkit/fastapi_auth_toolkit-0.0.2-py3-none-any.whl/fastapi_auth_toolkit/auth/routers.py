from fastapi import APIRouter

from fastapi_auth_toolkit.auth.api.auth import user_auth_router

auth_router = APIRouter(prefix="/auth", tags=["User Authentication"])

auth_router.include_router(user_auth_router)
