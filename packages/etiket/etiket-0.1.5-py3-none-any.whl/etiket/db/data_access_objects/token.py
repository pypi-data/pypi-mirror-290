from etiket.exceptions.exceptions import TokenAbuseException
from etiket.db.data_models.token import TokenInternal, RefreshToken
from etiket.db.models import Tokens

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from etiket.db.data_access_objects.base import dao_base

import logging

logger = logging.getLogger(__name__)
class dao_token(dao_base):
    @staticmethod
    def new(user_id:int , session : Session):
        tokenInternal = TokenInternal(user_id=user_id)
        token =  dao_token._create(tokenInternal, Tokens, session)
        logger.info("New token created for user_id: %s", user_id, extra={'user_id': user_id, 'session_id': token.session_id, 'token_id': token.token_id})
        return token.session_id, token.token_id
    
    @staticmethod
    def renew(session_id : int, token_id : int, session : Session):
        logger.info("Renewing token for session_id: %s, token_id: %s", session_id, token_id, extra={'session_id': session_id, 'token_id': token_id})
        stmt = select(Tokens).where(Tokens.session_id == session_id)
        token = session.execute(stmt).scalar_one_or_none()

        if not token or token.token_id != token_id:
            if token:
                dao_token._delete(Tokens, Tokens.session_id==token.session_id, session)
            logger.warning("Token abuse detected!", extra={'session_id': session_id, 'token_id': token_id})
            raise TokenAbuseException

        token.token_id += 1
        session.commit()
        return token.session_id, token.token_id