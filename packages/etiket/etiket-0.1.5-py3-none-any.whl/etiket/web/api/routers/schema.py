from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_scope_admin, is_admin, is_admin_type

from fastapi import APIRouter, Depends, Path, Query, status

from etiket.db.data_access_objects.schema import dao_schema

from etiket.db.data_models.schema import SchemaCreate, SchemaReadWithScopes, SchemaUpdate, SchemaRead
from etiket.db.data_models.token import AccessToken
from etiket.exceptions.exceptions import AdminUserException

from typing import List, Optional
import uuid

router = APIRouter(tags=["schema"])

# TODO redisign permissions on reading schemas.

@router.post("/schema/", status_code=status.HTTP_201_CREATED)
def create_schema(*, userCreate: SchemaCreate,
                        accessToken: AccessToken = Depends(is_scope_admin),
                        session: Session = Depends(get_db_session) ):
    dao_schema.create(userCreate, session)

@router.get("/schema/", response_model=SchemaReadWithScopes)
def get_schema(*, schema_uuid: uuid.UUID,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    return dao_schema.read(schema_uuid, session)

@router.get("/schemas/", response_model=List[SchemaReadWithScopes])
def get_schemas(*, schemaname_query : Optional[str] = None,
                        offset: int = 0,
                        limit: Optional[int] = None,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    return dao_schema.read_all(schemaname_query=schemaname_query, offset=offset,
                                limit=limit, session=session)

@router.patch("/schema/", status_code=status.HTTP_202_ACCEPTED)
def update_schema(*, schema_uuid: uuid.UUID,
                         schemaUpdate: SchemaUpdate,
                         accessToken: AccessToken = Depends(is_scope_admin),
                         session: Session = Depends(get_db_session) ):
    dao_schema.update(schema_uuid, schemaUpdate, session)

@router.delete("/schema/", status_code=status.HTTP_202_ACCEPTED)
def delete_schema(*, schema_uuid: uuid.UUID,
                         accessToken: AccessToken = Depends(is_scope_admin),
                         session: Session = Depends(get_db_session) ):
    dao_schema.delete(schema_uuid, session)