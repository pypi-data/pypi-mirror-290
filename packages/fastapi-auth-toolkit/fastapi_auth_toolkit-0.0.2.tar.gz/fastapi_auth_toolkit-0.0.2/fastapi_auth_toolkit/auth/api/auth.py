from fastapi import APIRouter, HTTPException, status, Request

from fastapi_auth_toolkit.auth.helpers.authentication import authenticate
from fastapi_auth_toolkit.auth.models.auth import AuthModel
from fastapi_auth_toolkit.auth.schemas.auth import UserRegisterSchema, UserLoginSchema
from fastapi_auth_toolkit.auth.schemas.response.auth import UserRegisterSuccessSchema, UserLoginSuccessSchema

user_auth_router = APIRouter()


@user_auth_router.post("/register", response_model=UserRegisterSuccessSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_register: UserRegisterSchema):
    try:
        # Use AuthModel's class method to create a new user
        created_user = await AuthModel.objects.create_user(**user_register.dict())
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_auth_router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(request: Request, user_login: UserLoginSchema):
    try:
        # Use AuthModel's class method to create a new user
        user_obj = await authenticate(
            request=request,
            email=user_login.email,
            password=user_login.password,
        )

        user_details = await UserLoginSuccessSchema.from_user_obj(user_obj)

        # Convert response to dictionary
        response_dict = user_details.dict()

        if not user_details.token:
            response_dict.pop('token', None)  # Remove 'token' key if it does not exist

        return response_dict

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
