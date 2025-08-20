from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRequestRegister(UserLogin):
    first_name: str
    last_name: str


class UserRegister(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class UserWithHashedPassword(User):
    hashed_password: str
