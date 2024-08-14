from etiket.exceptions.exceptions import TokenExpiredException,\
    AccessTokenExpectedException, RefreshTokenExpectedException
from etiket.db.types import UserType, TokenType

from pydantic import BaseModel, field_validator, Field, ConfigDict

import datetime, typing

class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int
    token_type: str = "bearer"

class AccessToken(BaseModel):
    sub : str
    exp : int
    user_type : UserType
    token_type : TokenType
    
    @field_validator('token_type')
    @classmethod
    def check_type(cls, v: TokenType):
        if TokenType.access != v:
            raise AccessTokenExpectedException
        return v
    
    @field_validator('exp')
    @classmethod
    def check_exp(cls, expiration_time: int) -> int:
        if expiration_time < int(datetime.datetime.now().timestamp()):
            raise TokenExpiredException
        return expiration_time

class RefreshToken(BaseModel):
    session_id : int
    token_id : int
    sub : str
    token_type : TokenType
    
    @field_validator('token_type')
    @classmethod
    def check_type(cls, v: TokenType):
        if TokenType.refresh != v:
            raise RefreshTokenExpectedException
        return v

class TokenInternal(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    session_id : typing.Optional[int] = Field(default=None)
    token_id   : int = Field(default=0)
    user_id    : int

