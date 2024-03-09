from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    # created_at: date
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # type: ignore