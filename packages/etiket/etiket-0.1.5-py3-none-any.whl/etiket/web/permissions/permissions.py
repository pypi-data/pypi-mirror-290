from etiket.db.data_models.token import AccessToken

from etiket.exceptions.exceptions import InvalidAccessTokenException,\
    InsufficientPrivigesException, UserIsNotOfAdminTypeException
from etiket.db.types import UserType
from etiket.settings import settings

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/token")

def retrieve_token_data(access_token: str = Depends(oauth2_scheme)):
    try:
        content = jwt.decode(access_token,
                                key = settings.ETIKET_TOKEN_SECRET_KEY,
                                algorithms = [settings.ETIKET_TOKEN_ALGORITHM])
        return AccessToken.model_validate(content)
    except:
        raise InvalidAccessTokenException

def is_any(accessToken : AccessToken  = Depends(retrieve_token_data)):
    return accessToken

def is_standard_user(accessToken : AccessToken = Depends(retrieve_token_data)):
    if accessToken.user_type not in [UserType.standard_user, UserType.superuser]:
        raise InsufficientPrivigesException(UserType.standard_user)
    return accessToken

def is_scope_admin(accessToken : AccessToken = Depends(retrieve_token_data)):
    if accessToken.user_type not in [UserType.scope_admin, UserType.superuser]:
        raise InsufficientPrivigesException(UserType.scope_admin)
    return accessToken

def is_admin(accessToken : AccessToken = Depends(retrieve_token_data)):
    if accessToken.user_type not in [UserType.admin, UserType.superuser]:
        raise InsufficientPrivigesException(UserType.admin)
    return accessToken

def is_super(accessToken : AccessToken = Depends(retrieve_token_data)):
    if accessToken.user_type != UserType.superuser:
        raise InsufficientPrivigesException(UserType.superuser)
    return accessToken

def is_admin_type(accessToken : AccessToken = Depends(retrieve_token_data)):
    if accessToken.user_type != UserType.standard_user:
        return accessToken
    else:
        raise UserIsNotOfAdminTypeException