from sqlalchemy.orm import Session
from sqlalchemy import select, update
from typing import Optional, List

from etiket.exceptions.exceptions import UserLogNotFoundException
from etiket.db.models import userLogs, UserLogStatus, Users
from etiket.db.data_models.user_logs import UserLogRead
from etiket.db.data_access_objects.user import _get_user_raw

class dao_user_logs:
    @staticmethod
    def create(user_name : str, key : str, reason : Optional[str], session:Session):
        user_id = _get_user_raw(user_name, session).id
        
        log = userLogs(user_id=user_id, key=key, reason=reason, status=UserLogStatus.pending)
        session.add(log)
        session.commit()
    
    @staticmethod
    def confirm(key : str, user_name : str, session:Session):
        user_id = _get_user_raw(user_name, session).id
        
        stmt = select(userLogs).where(userLogs.key == key).where(userLogs.user_id == user_id)
        result = session.execute(stmt).one_or_none()
        
        if result is None:
            raise UserLogNotFoundException(key, user_name)
        
        stmt = update(userLogs).where(userLogs.key == key).where(userLogs.user_id == user_id).values(status=UserLogStatus.secured)
        session.execute(stmt)
        session.commit()
        
    @staticmethod
    def read(user_name : str, offset : int, limit : int, session:Session) -> List[UserLogRead]:
        user_id = _get_user_raw(user_name, session).id
        
        stmt = select(userLogs).where(userLogs.user_id == user_id).offset(offset).limit(limit)
        stmt = stmt.order_by(userLogs.created.desc())
        result =  session.execute(stmt).scalars().all()

        return [UserLogRead.model_validate(r) for r in result]

    @staticmethod
    def read_many(user_name_query : Optional[str], offset : int, limit : int, session:Session) -> List[UserLogRead]:
        stmt = select(userLogs).join(userLogs.user)
        if user_name_query is not None:
            stmt = stmt.where(Users.username.ilike(f"{user_name_query}%"))
        stmt = stmt.offset(offset).limit(limit)
        stmt = stmt.order_by(userLogs.created.desc())
        result =  session.execute(stmt).scalars().all()

        return [UserLogRead.model_validate(r) for r in result]