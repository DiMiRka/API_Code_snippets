from pydantic import BaseModel, EmailStr

from src.models.user import RoleEnum


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: RoleEnum


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
