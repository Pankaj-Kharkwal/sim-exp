from pydantic import BaseModel


class Token(BaseModel):
    """
    Token response schema for OAuth2 authentication.
    """
    access_token: str
    token_type: str
    refresh_token: str | None = None


class TokenPayload(BaseModel):
    """
    Token payload schema.
    """
    sub: str | None = None
    type: str | None = "access"


class RefreshTokenRequest(BaseModel):
    """
    Refresh token request schema.
    """
    refresh_token: str
