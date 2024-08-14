from fastapi_auth_toolkit.app.events import EventManager
from fastapi_auth_toolkit.auth.events.profile import create_user_profile_event

from fastapi_auth_toolkit.auth.managers.auth import AuthManager
from fastapi_auth_toolkit.auth.managers.profile import UserProfileManager

from fastapi_auth_toolkit.auth.models.auth import AuthModel
from fastapi_auth_toolkit.auth.models.profile import UserProfileModel

# setting manager
AuthModel.set_manager(AuthManager)
UserProfileModel.set_manager(UserProfileManager)

# Register the listener to the 'created_user_profile' event
EventManager.register('created_user_profile', create_user_profile_event)
