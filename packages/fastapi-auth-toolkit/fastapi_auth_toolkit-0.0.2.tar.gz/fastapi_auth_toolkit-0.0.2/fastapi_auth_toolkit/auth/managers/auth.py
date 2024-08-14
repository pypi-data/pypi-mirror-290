from fastapi_auth_toolkit.app.events import EventManager
from fastapi_auth_toolkit.auth.exception.authentication import AccountAlreadyExistsException, AccountNotExistsException, PasswordInvalidException
from fastapi_auth_toolkit.auth.managers.base import BaseModelManager


class AuthManager(BaseModelManager):

    async def get_user_by_email(self, email: str):
        existing_user = await self.model.find_one({"email": email})
        if existing_user:
            return existing_user
        return None

    async def create_user(self, **extra_fields):
        """
        Create a new user with a hashed password.

        :param extra_fields: Keyword arguments containing user fields, including 'password'.
        :return: The created user document.
        :raises AccountAlreadyExistsException: If the email already exists or there is an error creating the user.
        """
        # Check if password is provided
        if 'password' not in extra_fields or not extra_fields['password']:
            raise ValueError('Password should not be None or empty.')

        email = extra_fields.get('email')
        if not email:
            raise ValueError('Email should be provided.')

        # Check if a user with the same email already exists
        user_account_obj = await self.get_user_by_email(email)
        if user_account_obj is not None:
            raise AccountAlreadyExistsException(message="User with this email already exists.")

        # Create a user instance with the provided fields
        new_user_obj = self.model(**extra_fields)

        # Assuming the model has a method to set and hash the password
        new_user_obj.set_password(extra_fields['password'])

        # Save the user document asynchronously
        await new_user_obj.insert()

        # Trigger the 'created_user_profile' event
        EventManager.trigger('created_user_profile', new_user_obj.id, new_user_obj.email)

        return new_user_obj

