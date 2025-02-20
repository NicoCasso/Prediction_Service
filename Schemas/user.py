
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserBase(BaseModel):
    username: Optional[str] = "rien"
    email: EmailStr
    role: str = "user"
    is_active: bool = False
    must_change_password: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    loans: List["LoanRequest"] = []

    class Config:
        from_attributes = True

class LoanRequest(BaseModel):
    id: int
    user_id: int
    amount: float
    status: str

    class Config:
        from_attributes = True
