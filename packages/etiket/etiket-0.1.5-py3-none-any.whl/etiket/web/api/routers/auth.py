from etiket.exceptions.exceptions import IncorrectUsernamePasswordException, ValidationCredentialsException

from etiket.db.get_db_session import Session, get_db_session

from etiket.db.data_access_objects.user import dao_user
from etiket.db.data_models.token import Token

from etiket.web.token.generation import create_token_by_username, create_token_by_refresh_token
from etiket.web.token.token_request_form import OAuth2TokenRequestForm

from fastapi import APIRouter, Depends

import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["token"])

@router.post("/token", response_model=Token,)
def get_token(form_data: OAuth2TokenRequestForm = Depends(),
                    session: Session = Depends(get_db_session),):
    if form_data.grant_type == "password":
        logger.info("Authenticating user with username: %s using password grant type", form_data.username)
        auth = dao_user.authenticate(form_data.username, form_data.password, session)
        if auth == False:
            logger.info("Authentication failed for user with username: %s", form_data.username, extra={'username': form_data.username})
            raise IncorrectUsernamePasswordException
        return create_token_by_username(form_data.username, session)
    elif form_data.grant_type == "refresh_token":
        logger.info("Refreshing token for user with username: %s using refresh token grant type", form_data.username)
        return create_token_by_refresh_token(form_data.refresh_token, session)
    else:
        raise ValidationCredentialsException