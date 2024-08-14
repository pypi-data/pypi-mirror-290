import secrets
from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class SessionSettings(BaseModel):
    """
    Configuration settings for managing session-based authentication.

    Attributes:
        expires_time (timedelta): The duration for which the session cookie should be valid.
                                   Default is 2 hours (7200 seconds).
        httponly (bool): If True, the cookie is HTTP-only, which helps prevent access by JavaScript
                         and mitigates XSS attacks. Default is True.
        secure (bool): If True, the cookie is only sent over HTTPS connections. Set to True if your
                       application is served over HTTPS. Default is False.
        samesite (str | None): Controls the cookie's cross-site sending policy. Can be 'Lax', 'Strict',
                               or 'None'. 'Lax' provides basic CSRF protection, 'Strict' provides
                               stricter protection, and 'None' disables SameSite policy. Default is 'Lax'.
        secret_key (str): A secret key used for encoding or decoding session data. Defaults to a
                          randomly generated URL-safe token.

    """
    expires_time: timedelta = timedelta(hours=2)  # Duration for cookie validity (2 hours by default)
    httponly: bool = True  # Prevents cookie access via JavaScript
    samesite: Optional[str] = 'Lax'  # SameSite attribute for CSRF protection; 'None' disables SameSite
    secret_key: str = secrets.token_urlsafe(32)  # Secret key for encoding/decoding session data

    class Config:
        """
        Configuration settings for Pydantic model behavior.
        """
        extra = "ignore"  # Ignore extra fields that are not defined in the model
