from fastapi_auth_toolkit.app.utils.enums.base import BaseCustomEnum


class UserActionTypeEnum(BaseCustomEnum):
    ACCOUNT_CREATED = 'Account created successfully'
    ACCOUNT_VARIFED = 'Account verified successfully'
    ACCOUNT_DEACTIVATED = 'Account deactivated successfully'
    ACCOUNT_REACTIVATED = 'Account reactivated successfully'
    PASSWORD_CHANGED = 'Your password has been changed successfully'
    ACCOUNT_DELETED = 'Account deleted successfully'
    PROFILE_UPDATED = 'Your profile has been updated successfully'
    USERNAME_CHANGED = 'Username has been changed successfully'
    EMAIL_CHANGED = 'Email has been changed successfully'
    PHONE_NUMBER_CHANGED = 'Phone number has been changed successfully'
    TWO_FACTOR_AUTHENTICATION_ACTIVATED = 'Two factor authentication has been activated successfully'
    TWO_FACTOR_AUTHENTICATION_DEACTIVATED = 'Two factor authentication has been deactivated successfully'
    LOGIN_SUCCESS = "You have been logged in"
    LOGOUT = "Logged out successfully"
    OTHER = "other"
