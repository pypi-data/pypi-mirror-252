"""Authentication Schemas."""

from fastapi import Form
from pydantic import BaseModel, SecretStr

from . import EmailStr


class AuthenticationToken(BaseModel):
    """Authentication token schema."""

    access_token: str
    """The access token."""
    refresh_token: str
    """The refresh token."""
    expires_in: int
    """The number of seconds until the access token expires."""
    token_type: str
    """The token type."""


class LoginForm:
    """Login credentials schema."""

    def __init__(self, username: EmailStr = Form(), password: SecretStr = Form()):
        """
        Creates the below login form parameters when used as a dependency in a route.

        Parameters
        ----------
            `username` (`EmailStr`): the username

            `password` (`SecretStr`): the password
        """
        self.username = username
        self.password = password


class ForgotPassword(BaseModel):
    """Forgot password schema."""

    email: EmailStr
    """The email address of the user."""


class ResetPassword(BaseModel):
    """Reset password schema."""

    token: str
    """The token used to reset the password."""
    password: SecretStr
    """The new password."""
