from typing import Optional

from pydantic import BaseModel


# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str


class UserChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str
