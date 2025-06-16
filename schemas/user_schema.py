from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    name: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    name: str
