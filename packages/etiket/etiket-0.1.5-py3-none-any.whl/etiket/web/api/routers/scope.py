from etiket.exceptions.exceptions import UserNotInScopeException
from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_scope_admin, is_admin, is_admin_type, UserType

from fastapi import APIRouter, Depends, Query, status

from etiket.db.data_access_objects.scope import dao_scope

from etiket.db.data_models.scope import ScopeRead, ScopeReadWithUsers, ScopeCreate, ScopeUpdate
from etiket.db.data_models.token import AccessToken

from typing import List, Optional

import uuid

router = APIRouter(tags=["scope"])

@router.post("/scope/", status_code=status.HTTP_201_CREATED)
def create_scope(scopeCreate: ScopeCreate,
                        accessToken: AccessToken = Depends(is_admin_type),
                        session: Session = Depends(get_db_session) ):
    dao_scope.create(scopeCreate, accessToken.sub, session)
    dao_scope.assign_user(scopeCreate.uuid, accessToken.sub, session)

@router.get("/scope/", response_model=ScopeReadWithUsers)
def get_scope(*, scope_uuid: uuid.UUID,
                    accessToken: AccessToken = Depends(is_any),
                    session: Session = Depends(get_db_session) ):
    response = dao_scope.read(scope_uuid, session=session)
    if not dao_scope.user_in_scope(scope_uuid, username=accessToken.sub, session=session):
        raise UserNotInScopeException(accessToken.sub)
    return response

@router.patch("/scope/", status_code=status.HTTP_200_OK)
def update_scope(*, scope_uuid: uuid.UUID,
                        scopeUpdate: ScopeUpdate,
                        accessToken: AccessToken = Depends(is_scope_admin),
                        session: Session = Depends(get_db_session) ):
    dao_scope.update(scope_uuid, scopeUpdate, session)

@router.delete("/scope/", status_code=status.HTTP_200_OK)
def delete_scope(*, scope_uuid: uuid.UUID,
                        accessToken: AccessToken = Depends(is_scope_admin),
                        session: Session = Depends(get_db_session) ):
    dao_scope.delete(scope_uuid, session)

# @ alberto would it be handiest if this one also returns the users -- now added?
@router.get("/scopes/", response_model=List[ScopeReadWithUsers])
def get_scopes(*, name: Optional[str] = Query(None, max_length=100),
                        offset: int = 0,
                        limit: Optional[int] = None,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    if accessToken.user_type == UserType.admin:
        return dao_scope.read_all(name_query=name, offset=offset, limit=limit, session=session)
    else:
        return dao_scope.read_all(name_query=name, username=accessToken.sub,
                                   offset=offset, limit=limit, session=session)

@router.put("/scope/assign_members/", status_code=status.HTTP_202_ACCEPTED)
def assign_user_to_scope(*, scope_uuid: uuid.UUID,
                               username : str =  Query(..., min_length=3, max_length=100),
                               accessToken: AccessToken = Depends(is_any),
                               session: Session = Depends(get_db_session) ):
    if accessToken.user_type != UserType.admin:
        if not dao_scope.user_in_scope(scope_uuid, username=accessToken.sub, session=session):
            raise UserNotInScopeException(accessToken.sub)
    dao_scope.assign_user(scope_uuid, username, session)

@router.delete("/scope/remove_members/", status_code=status.HTTP_202_ACCEPTED)
def remove_user_from_scope(*, scope_uuid: uuid.UUID,
                               username : str =  Query(..., min_length=3, max_length=100),
                               accessToken: AccessToken = Depends(is_admin_type),
                               session: Session = Depends(get_db_session) ):
    if accessToken.user_type != UserType.admin:
        if not dao_scope.user_in_scope(scope_uuid, username=accessToken.sub, session=session):
            raise UserNotInScopeException(accessToken.sub)
    dao_scope.remove_user(scope_uuid, username, session)

@router.put("/scope/assign_schema/", status_code=status.HTTP_202_ACCEPTED)
def assign_schema_to_scope(*, scope_uuid: uuid.UUID,
                               schema_uuid : uuid.UUID,
                               accessToken: AccessToken = Depends(is_scope_admin),
                               session: Session = Depends(get_db_session) ):
    dao_scope.assign_schema(scope_uuid, schema_uuid, session)

@router.delete("/scope/remove_schema/", status_code=status.HTTP_202_ACCEPTED)
def remove_schema_from_scope(*, scope_uuid: uuid.UUID,
                               schema_uuid : uuid.UUID,
                               accessToken: AccessToken = Depends(is_scope_admin),
                               session: Session = Depends(get_db_session) ):
    dao_scope.remove_schema(scope_uuid, schema_uuid, session)