from etiket.exceptions.exceptions import InvalidRefreshTokenException, UserDisabledException

from etiket.db.data_access_objects.user import _get_user_raw
from etiket.db.data_access_objects.token import dao_token
from etiket.db.data_models.user import UserReadWithScopes
from etiket.db.data_models.token import Token, AccessToken, RefreshToken
from etiket.db.types import TokenType
from etiket.settings import settings

import jwt, datetime, logging

logger = logging.getLogger(__name__)

def create_token_by_username(username: str, session):
    user = _get_user_raw(username, session=session)
    _validate_user(user)
    session_id, token_id = dao_token.new(user.id, session)
    
    return _generate_access_and_refresh_tokens(user, session_id, token_id)

def create_token_by_refresh_token(refresh_token : str, session):
    try :
        content = jwt.decode(refresh_token,
                             key = settings.ETIKET_TOKEN_SECRET_KEY,
                             algorithms = [settings.ETIKET_TOKEN_ALGORITHM])
        refresh_token = RefreshToken(**content) #TODO I removed validations bc it was throwing error
    except Exception:
        logger.exception("Error while decoding refresh token")
        raise InvalidRefreshTokenException
    
    session_id, token_id = dao_token.renew(refresh_token.session_id ,refresh_token.token_id, session)
    user = _get_user_raw(refresh_token.sub, session=session)
    _validate_user(user)
    
    return _generate_access_and_refresh_tokens(user, session_id, token_id)

def _validate_user(user : UserReadWithScopes):
    if user.active == False:
        raise UserDisabledException(user.username)
    if user.disable_on:
        if user.disable_on > datetime.datetime.now():
            raise UserDisabledException(user.username)

def _generate_access_and_refresh_tokens(user : UserReadWithScopes, session_id : int, token_id : int):
    exp_date = int(datetime.datetime.now().timestamp() + 
                settings.ETIKET_TOKEN_EXPIRE_MINUTES*60)
        
    accessToken = AccessToken(sub=user.username,
                              exp=exp_date, 
                              user_type=user.user_type,
                              token_type=TokenType.access)
    refreshToken = RefreshToken(session_id=session_id,
                                token_id=token_id,
                                sub=user.username,
                                token_type=TokenType.refresh)
    
    access_token = jwt.encode(accessToken.model_dump(),
                                key = settings.ETIKET_TOKEN_SECRET_KEY,
                                algorithm = settings.ETIKET_TOKEN_ALGORITHM)
    refresh_token = jwt.encode(refreshToken.model_dump(),
                                key = settings.ETIKET_TOKEN_SECRET_KEY,
                                algorithm = settings.ETIKET_TOKEN_ALGORITHM)

    return Token(access_token=access_token, refresh_token=refresh_token, expires_at=exp_date)