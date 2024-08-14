import secrets
from datetime import timedelta

from pydantic import BaseModel


class CookieSettings(BaseModel):
    """
    Configuration settings for cookies used in authentication.

    Attributes:
        expires_time (timedelta): The duration for which the cookie should be valid.
                                   Default is 5 minutes.
        cookie_name (str): The name of the cookie. Default is 'user_id'.
        httponly (bool): Flag indicating whether the cookie should be HTTP-only.
                         If True, prevents JavaScript access to the cookie, helping
                         to prevent XSS attacks. Default is True.
        cookie_secure (bool): Flag indicating whether the cookie should be sent
                              only over secure (HTTPS) connections. Set to True
                              for HTTPS environments. Default is False.
        samesite (str | None): Attribute for controlling cookie sending policy
                               in cross-site requests. Can be 'Lax', 'Strict', or
                               'None'. 'Lax' is the default and provides basic CSRF
                               protection. Set to 'None' if no SameSite policy is desired.

    """
    expires_time: timedelta = timedelta(days=1)  # Duration for cookie validity
    cookie_name: str = "user_id"  # Name of the cookie
    httponly: bool = True  # Prevents access to cookie via JavaScript (XSS protection)
    cookie_secure: bool = False  # Cookie is sent only over HTTPS if True
    samesite: str | None = 'Lax'  # SameSite attribute for CSRF protection; 'None' disables SameSite
    secret_key: str = secrets.token_urlsafe(32)  # Secret key for encoding/decoding JWT

    class Config:
        """
        Configuration for Pydantic model behavior.
        """
        extra = "ignore"  # Ignore any extra fields that are not defined in the model
