from etiket.exceptions.exceptions import ScopeDoesNotExistException,\
    UserAlreadyPartOfScopeException, UserAlreadyNotPartOfScopeException,\
    SchemaAlreadyAssignedException, ScopeDoesAlreadyExistException,\
    CannotDeleteAScopeWithDatasetsException, MemberHasNoBusinessInThisScopeException

from etiket.db.data_models.scope import ScopeUpdate, ScopeCreate, ScopeReadWithUsers
from etiket.db.models import Scopes, Datasets, Users

from etiket.db.data_access_objects.schema import _get_schema_raw
from etiket.db.data_access_objects.user import _get_user_raw, UserType
from etiket.db.data_access_objects.base import dao_base
from etiket.db.data_access_objects.S3_utility import _get_bucket_raw, check_user_has_access_to_bucket
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from typing import Optional, List
from uuid import UUID

class dao_scope(dao_base):
    @staticmethod
    def create(scopeCreate : ScopeCreate, creator : str, session: Session):
        if not dao_scope._unique(Scopes, Scopes.uuid == scopeCreate.uuid, session):
            raise ScopeDoesAlreadyExistException(scopeCreate.uuid)
        
        check_user_has_access_to_bucket(scopeCreate.bucket_uuid, username=creator, session=session)
        bucket_id = _get_bucket_raw(scopeCreate.bucket_uuid, session).id
        
        new_scope = Scopes(**scopeCreate.model_dump(exclude=["bucket_uuid"]), bucket_id=bucket_id)
        session.add(new_scope)
        session.commit()
        
    @staticmethod
    def read(scope_uuid : UUID, session : Session):
        scope = _get_scope_raw(scope_uuid=scope_uuid, session=session, lazy=False)
        return ScopeReadWithUsers.model_validate(scope)
    
    @staticmethod
    def read_all(name_query : str = None, archived : bool = None, username : str=None,
                 offset : int = None, limit :int=None, session : Session = None):
        stmt = dao_scope._query(Scopes, string_query = {Scopes.name : name_query},
                                            is_equal_query ={Scopes.archived : archived},
                                            orderby = Scopes.name, offset=offset, limit=limit)
        if username:
            stmt = stmt.join(Users.scopes).where(Users.username==username)
        stmt = stmt.options(selectinload(Scopes.users))
        result = session.execute(stmt).scalars().all()
        return [ScopeReadWithUsers.model_validate(res) for res in result]

    @staticmethod
    def update(scope_uuid : UUID, scopeUpdate : ScopeUpdate, session : Session):
        scope = _get_scope_raw(scope_uuid, session)
        return dao_scope._update(scope, scopeUpdate, session)

    @staticmethod
    def delete(scope_uuid : UUID, session : Session):
        scope = _get_scope_raw(scope_uuid, session)
        
        if _n_datasets_in_scope(scope, session) != 0:
            raise CannotDeleteAScopeWithDatasetsException(scope.name)
        
        session.delete(scope)
        session.commit()
    
    @staticmethod
    def user_in_scope(scope_uuid : UUID, username : str, session : Session):
        stmt = select(func.count(Scopes.id)).where(Scopes.uuid==scope_uuid)
        stmt = stmt.join(Users.scopes).where(Users.username==username)     
        if session.execute(stmt).scalar_one() == 0:
            return False
        return True
        
    @staticmethod
    def assign_user(scope_uuid : UUID, username : str, session : Session):
        user  = _get_user_raw(username, session)
        scope = _get_scope_raw(scope_uuid, session, lazy=False)

        if user in scope.users:
            raise UserAlreadyPartOfScopeException(username, scope.name)
        
        scope.users.append(user)
        session.commit()
    
    @staticmethod
    def remove_user(scope_uuid : UUID, username : str, session : Session):
        scope = _get_scope_raw(scope_uuid, session, lazy=False)
        user  = _get_user_raw(username, session)

        if user not in scope.users:
            raise UserAlreadyNotPartOfScopeException(username, f"{scope.name} ({scope.uuid})")
        
        scope.users.remove(user)
        session.commit()
    
    @staticmethod
    def assign_schema(scope_uuid : UUID, schema_uuid : UUID, session : Session):
        schema  = _get_schema_raw(schema_uuid, session)
        scope = _get_scope_raw(scope_uuid, session, lazy=False)

        if scope.schema is not None:
            if scope.schema.uuid == schema.uuid:
                raise SchemaAlreadyAssignedException(schema.name, scope.name)
        
        scope.schema = schema
        session.commit()
        
    @staticmethod
    def remove_schema(scope_uuid : UUID, session : Session):
        scope = _get_scope_raw(scope_uuid, session, lazy=False)
        scope.schema = None
        session.commit()
    
    @staticmethod  
    def validate_scope(scope_uuid : UUID, username : str, user_type:UserType, session:Session) -> int:
        scope_uuids_user = _get_user_scopes_raw(username, user_type, session)
        
        for scope in scope_uuids_user:
            if scope.uuid == scope_uuid:
                return scope.id

        raise MemberHasNoBusinessInThisScopeException(scope_uuid)
        
    @staticmethod
    def validate_scopes(scope_uuids : Optional[List[UUID]], username : str, user_type:UserType, session:Session) -> List[int]:
        scope_uuids_user = _get_user_scopes_raw(username, user_type, session)
        
        if scope_uuids:
            scope_dict = {scope.uuid: scope for scope in scope_uuids_user}
            if not set(scope_uuids).issubset(scope_dict.keys()):
                raise MemberHasNoBusinessInThisScopeException(set(scope_uuids).difference(scope_dict))
            return [scope_dict[scope_uuid].id for scope_uuid in scope_uuids]

        return [scope.id for scope in scope_uuids_user]

def _get_user_scopes_raw(username : str, user_type:UserType, session:Session) -> List[Scopes] :
    if user_type in [UserType.standard_user, UserType.scope_admin]:
        stmt = select(Scopes).join(Users.scopes).where(Users.username==username)
        scopes = session.execute(stmt).scalars().all()
    else: # skips validation for admin users
        scopes = session.execute(select(Scopes)).scalars().all()
        
    return scopes
       
def _get_scope_raw(scope_uuid : UUID, session:Session, lazy=True) -> Scopes:
    stmt = select(Scopes).where(Scopes.uuid == scope_uuid)
    if lazy == False:
        stmt.options(selectinload(Scopes.users))
    result = session.execute(stmt).scalar_one_or_none()
    
    if result:
        return result
    raise ScopeDoesNotExistException()


def _n_datasets_in_scope(scope : Scopes, session:Session):
    stmt = select(func.count(Datasets.id)).where(Datasets.scope_id == scope.id)
    return session.execute(stmt).scalar_one()