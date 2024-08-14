import uuid

from fastapi import APIRouter, status, Depends
from typing import List

from etiket.db.data_models.token import AccessToken
from etiket.db.data_models.S3 import (
    S3ResourceRead, S3BucketRead,
    S3ResourceCreate, S3ResourceUpdate, S3ResourcePermission,
    S3TransferStatus
)
from etiket.db.data_access_objects.S3 import dao_S3_resources, dao_S3_buckets, dao_S3_transfers

from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_admin_type

router = APIRouter(tags=["S3 Management"])

# Resources Endpoints
@router.get("/S3/resource/read/", response_model=List[S3ResourceRead])
async def read_s3_resources(*, 
                        accessToken: AccessToken = Depends(is_admin_type),
                        session: Session = Depends(get_db_session) ):
    return dao_S3_resources.read(accessToken.sub, accessToken.user_type, session)

@router.post("/S3/resource/create/", status_code=status.HTTP_201_CREATED)
async def create_s3_resource(new_resource: S3ResourceCreate, 
                             accessToken: AccessToken = Depends(is_admin_type),
                             session: Session = Depends(get_db_session)):
    dao_S3_resources.create(new_resource, accessToken.sub, session)

@router.patch("/S3/resource/update/", status_code=status.HTTP_200_OK)
async def update_s3_resource(resource_uuid: uuid.UUID,
                             updated_resource: S3ResourceUpdate,
                             accessToken: AccessToken = Depends(is_admin_type),
                             session: Session = Depends(get_db_session)):
    dao_S3_resources.update(resource_uuid, updated_resource, accessToken.sub, session)

@router.post("/S3/resource/grant_access/", status_code=status.HTTP_202_ACCEPTED)
async def grant_access_to_resource(target_user: str,
                                  resource_uuid: uuid.UUID,
                                  permissions: S3ResourcePermission,
                                  accessToken: AccessToken = Depends(is_admin_type),
                                  session: Session = Depends(get_db_session)):
    dao_S3_resources.grant_access(target_user, resource_uuid, permissions, accessToken.sub, session)

@router.delete("/S3/resource/revoke_access/", status_code=status.HTTP_202_ACCEPTED)
async def revoke_access_to_resource(target_user: str,
                                      resource_uuid: uuid.UUID,
                                      accessToken: AccessToken = Depends(is_admin_type),
                                      session: Session = Depends(get_db_session)):
    dao_S3_resources.revoke_access(target_user, resource_uuid,  accessToken.sub, session)

# Buckets Endpoints
@router.get("/S3/bucket/read/", response_model=List[S3BucketRead])
async def read_s3_buckets(*,
                            accessToken: AccessToken = Depends(is_admin_type),
                            session: Session = Depends(get_db_session)):
    return dao_S3_buckets.read(accessToken.sub, accessToken.user_type, session)

@router.post("/S3/bucket/create/", status_code=status.HTTP_201_CREATED)
async def create_s3_bucket(resource_uuid: uuid.UUID, 
                           bucket_name: str,
                           accessToken: AccessToken = Depends(is_admin_type),
                           session: Session = Depends(get_db_session)):
    dao_S3_buckets.create(resource_uuid, bucket_name, accessToken.sub, session)

@router.post("/S3/bucket/add_existing/", status_code=status.HTTP_201_CREATED)
async def add_existing_s3_bucket(resource_uuid: uuid.UUID,
                                    bucket_name: str,
                                    accessToken: AccessToken = Depends(is_admin_type),
                                    session: Session = Depends(get_db_session)):
    dao_S3_buckets.add_existing(resource_uuid, bucket_name, accessToken.sub, session)

@router.post("/S3/bucket/grant_access/", status_code=status.HTTP_202_ACCEPTED)
async def grant_access_to_bucket(target_user: str,
                                  bucket_uuid: uuid.UUID,
                                  accessToken: AccessToken = Depends(is_admin_type),
                                  session: Session = Depends(get_db_session)):
    dao_S3_buckets.grant_access(target_user, bucket_uuid, accessToken.sub, session)

@router.delete("/S3/bucket/revoke_access/", status_code=status.HTTP_202_ACCEPTED)
async def revoke_access_to_bucket(target_user: str,
                                   bucket_uuid: uuid.UUID,
                                   accessToken: AccessToken = Depends(is_admin_type),
                                   session: Session = Depends(get_db_session)):
    dao_S3_buckets.revoke_access(target_user, bucket_uuid, accessToken.sub, session)

# Transfers Endpoints
@router.post("/S3/transfer/create/", status_code=status.HTTP_201_CREATED)
async def create_s3_transfer(scope_uuid: uuid.UUID,
                             bucket_uuid: uuid.UUID,
                             accessToken: AccessToken = Depends(is_admin_type),
                             session: Session = Depends(get_db_session)):
    dao_S3_transfers.transfer_data(scope_uuid, bucket_uuid, accessToken.sub, session)
        
@router.get("/S3/transfer/status-overview/", response_model=List[S3TransferStatus])
async def status_overview(*, 
                        accessToken: AccessToken = Depends(is_admin_type),
                        session: Session = Depends(get_db_session) ):
    return dao_S3_transfers.status_overview(accessToken.sub, accessToken.user_type, session)