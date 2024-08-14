from etiket.exceptions.exceptions import CannotCreateSuperUser

from etiket.db.data_models.user_base import UserBase, UserRead
from etiket.db.types import UserType, passwordstr
from etiket.db.data_models.scope import ScopeRead

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo

import datetime


class userTypeValidation:
    @field_validator('user_type')
    @classmethod
    def check_type(cls, userType: UserType, info: ValidationInfo):
        context = info.context
        if UserType.superuser == userType:
            if context and context["allow_sudo"] == True:
                pass
            else:
                raise CannotCreateSuperUser
        return userType

class UserCreate(UserBase, userTypeValidation):
    password : passwordstr
        
class UserReadWithScopes(UserRead):
    scopes : List[ScopeRead]

class UserUpdateMe(BaseModel):
    firstname: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)

class UserPasswordUpdate(BaseModel):
    username : str
    password : str
    new_password : passwordstr

class UserUpdate(UserUpdateMe):
    password : Optional[str] = Field(default=None)
    disable_on: Optional[datetime.datetime] = Field(default=None)    
    user_type: Optional[UserType] = Field(default=None)
    active : Optional[str] = Field(default=None)
    
class UserLogin(BaseModel):
    username : str
    password : str