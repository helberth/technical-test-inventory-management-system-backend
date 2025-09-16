from pydantic import BaseModel, EmailStr

# Base schema (atributos comunes)
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Pydantic V2

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenWithUser(Token):
    user: UserRead
