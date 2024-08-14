from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_scope_admin, is_admin, is_admin_type

from fastapi import APIRouter, Depends, Query, status

from etiket.db.data_access_objects.dataset import dao_dataset
from etiket.db.data_access_objects.scope import dao_scope
from etiket.db.data_models.dataset import DatasetCreate, DatasetRead, DatasetUpdate,\
                                        DatasetSearch, DatasetSelection

from etiket.db.data_models.token import AccessToken
from etiket.exceptions.exceptions import DatasetNotFoundExceptionUUIDAltUIDException, DatasetPresentInMultipleScopesException 

from typing import List, Optional
from zoneinfo import available_timezones

import datetime, uuid, sqlalchemy

router = APIRouter(tags=["datasets"])

# TODO : discuss with Arthur/Alberto to what the admin/scope admin should have access precisely.

@router.post("/dataset/", status_code=status.HTTP_201_CREATED)
def create_dataset(*, datasetCreate: DatasetCreate,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    dao_scope.validate_scope(datasetCreate.scope_uuid, accessToken.sub, accessToken.user_type, session)
    dao_dataset.create(datasetCreate, session)

@router.get("/dataset/", response_model=DatasetRead)
def read_dataset_by_uuid(*, dataset_uuid : uuid.UUID,
                        scope_uuid : Optional[uuid.UUID] = None,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    if scope_uuid is None:
        scope_ids = dao_scope.validate_scopes(scope_uuid, accessToken.sub, accessToken.user_type, session)
    else:
        scope_ids = [dao_scope.validate_scope(scope_uuid, accessToken.sub, accessToken.user_type, session)]
    dataset = dao_dataset.read(dataset_uuid, scope_ids, session=session)
    dao_scope.validate_scope(dataset.scope.uuid, accessToken.sub, accessToken.user_type, session)
    return dataset

@router.get("/dataset/by_uuid_or_alt_uid/", response_model=DatasetRead)
def read_dataset_by_uuid_or_uid(*, dataset_uuid_or_uid : 'str | uuid.UUID',
                                scope_uuid : Optional[uuid.UUID] = None,
                                accessToken: AccessToken = Depends(is_any),
                                session: Session = Depends(get_db_session) ):

    if scope_uuid is None:
        scope_ids = dao_scope.validate_scopes(scope_uuid, accessToken.sub, accessToken.user_type, session)
    else:
        scope_ids = [dao_scope.validate_scope(scope_uuid, accessToken.sub, accessToken.user_type, session)]
    
    datasets, _ = dao_dataset.search_for_uuid_or_uid(dataset_uuid_or_uid, scope_ids, session=session)

    if len(datasets) == 0:
        raise DatasetNotFoundExceptionUUIDAltUIDException(dataset_uuid_or_uid)
    if len(datasets) > 1:
        raise DatasetPresentInMultipleScopesException(datasets)
    return datasets[0]

@router.get("/dataset/by_alt_uid/", response_model=DatasetRead)
def read_dataset_by_alt_uid(*, dataset_alt_uid : str,
                                scope_uuid : uuid.UUID,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    scope_id = dao_scope.validate_scope(scope_uuid, accessToken.sub, accessToken.user_type, session)
    return dao_dataset.read_by_alt_uid(dataset_alt_uid, scope_id, session=session)

@router.patch("/dataset/", status_code=status.HTTP_200_OK)
def update_dataset(*, dataset_uuid : uuid.UUID,
                        datasetUpdate: DatasetUpdate,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    scope_uuid = dao_dataset.get_scope_uuid_from_ds_uuid(dataset_uuid, session)
    dao_scope.validate_scope(scope_uuid, accessToken.sub, accessToken.user_type, session)
    dao_dataset.update(dataset_uuid, datasetUpdate, session)

@router.delete("/dataset/", status_code=status.HTTP_200_OK)
def delete_dataset(*, dataset_uuid : uuid.UUID,
                        accessToken: AccessToken = Depends(is_scope_admin),
                        session: Session = Depends(get_db_session) ):
    scope_uuid = dao_dataset.get_scope_uuid_from_ds_uuid(dataset_uuid, session)
    dao_scope.validate_scope(scope_uuid, accessToken.sub, accessToken.user_type, session)
    dao_dataset.delete(dataset_uuid, session)

@router.post("/datasets/search/", response_model=List[DatasetRead])
def dataset_search(datasetSearch : DatasetSearch,
                        offset: int = 0,
                        limit: int = Query(default=50, le=1000),
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    scope_ids = dao_scope.validate_scopes(datasetSearch.scope_uuids, accessToken.sub, accessToken.user_type, session)
    if datasetSearch.search_query is not None:
        identifier_results, is_uuid = dao_dataset.search_for_uuid_or_uid(datasetSearch.search_query, scope_ids, session)
    else:
        identifier_results = []
        is_uuid = False
    
    if is_uuid:
        return identifier_results
    
    if offset > len(identifier_results):
        offset -= len(identifier_results)
    elif offset + limit <= len(identifier_results):
        return identifier_results[offset:offset+limit]
    else:
        identifier_results = identifier_results[offset:]
        limit = limit - len(identifier_results)
        offset = 0
    
    search_result = dao_dataset.search(datasetSearch, scope_ids, offset = offset, limit=limit, session=session)
    return identifier_results + search_result

@router.post("/datasets/distinct_dates/", response_model=List[datetime.date])
def dataset_get_distinct_dates(datasetSearch : DatasetSearch,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    if datasetSearch.time_zone in available_timezones():
        session.execute(sqlalchemy.text(f"SET TIME ZONE '{datasetSearch.time_zone}';"))
    scope_ids = dao_scope.validate_scopes(datasetSearch.scope_uuids, accessToken.sub, accessToken.user_type, session)
    session.execute(sqlalchemy.text("SET TIME ZONE 'UTC';"))
    return dao_dataset.get_distinct_dates(datasetSearch, scope_ids, session=session)

@router.post("/datasets/attributes/", response_model=dict[str, List[str]])
def dataset_get_attributes(*, datasetSelection : DatasetSelection,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    scope_ids = dao_scope.validate_scopes(datasetSelection.scope_uuids, accessToken.sub, accessToken.user_type, session)
    return dao_dataset.get_attributes(datasetSelection, scope_ids, session=session)

