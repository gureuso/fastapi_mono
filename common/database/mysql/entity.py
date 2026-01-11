from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserEntity(BaseModel):
    id: Optional[int] = None
    num: Optional[str] = Field(default=None, min_length=10, max_length=10)
    email: EmailStr
    provider: str
    created_at: datetime
