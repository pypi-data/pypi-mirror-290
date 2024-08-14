from typing import Optional

from pydantic import BaseModel, EmailStr, Field, constr

from fastapi_auth_toolkit.auth.models import AuthModel


class UserRegisterSchema(AuthModel):
    password: str


class UserLoginSchema(BaseModel):
    password: str = constr(min_length=3, max_length=64)
    email: EmailStr


class AccountUpdateSchema(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=25)
    first_name: str = Field(min_length=2, max_length=15)
    last_name: Optional[str] = Field(min_length=2, max_length=15)
    password: str


class UserLoginResponseSchema(BaseModel):
    pass
