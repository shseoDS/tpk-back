from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserOut(BaseModel):
    user_key: int
    email: str
    provider_type: Optional[str] = None
    ins_date: datetime


class SocialLoginRequest(BaseModel):
    email: str
    provider_id: str
    provider_type: str  # google, apple, kakao 등


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
