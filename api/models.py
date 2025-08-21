from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr

class UserCreate(User):
    password: str

class UserOut(User):
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True
