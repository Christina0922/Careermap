from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class RIASECScore(BaseModel):
    R: int = 0
    I: int = 0
    A: int = 0
    S: int = 0
    E: int = 0
    C: int = 0

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    riasec_scores: Optional[RIASECScore] = None

    class Config:
        from_attributes = True

