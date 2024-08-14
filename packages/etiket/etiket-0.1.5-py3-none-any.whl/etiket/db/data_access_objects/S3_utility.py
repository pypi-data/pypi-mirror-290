import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from etiket.db.data_access_objects.user import _get_user_raw
from etiket.exceptions.exceptions import (
    ResourceCannotBeAccessedException, BucketDoesNotExistException,
    ResourceDoesNotExistException, InsufficientPermissionsError,
)
from etiket.db.models import S3Resources, S3Buckets, Users, S3BucketPermissions

from etiket.db.types import UserType

def get_bucket_by_id(bucket_id : int, session : Session) -> S3Buckets:
    stmt = select(S3Buckets).where(S3Buckets.id == bucket_id)
    return session.execute(stmt).scalar_one()

def get_resource_by_id(resource_id : int, session : Session) -> S3Resources:
    stmt = select(S3Resources).where(S3Resources.id == resource_id)
    return session.execute(stmt).scalar_one()

def _get_resource_raw(resource_uuid: uuid.UUID, session : Session, load_buckets : bool = False, load_permissions : bool = False) -> S3Resources:
    stmt = select(S3Resources).where(S3Resources.resource_uuid == resource_uuid)
    if load_buckets:
        stmt = stmt.options(joinedload(S3Resources.buckets))
    if load_permissions:
        stmt = stmt.options(joinedload(S3Resources.permissions))
    res = session.execute(stmt).unique().scalar_one_or_none()
    if res is None:
        raise ResourceDoesNotExistException(resource_uuid)
    return res

def _get_bucket_raw(bucket_uuid: uuid.UUID, session : Session, load_permissions : bool = False) -> S3Buckets:
    stmt = select(S3Buckets).where(S3Buckets.bucket_uuid == bucket_uuid)
    if load_permissions:
        stmt = stmt.options(selectinload(S3Buckets.permissions))
    res = session.execute(stmt).scalar_one_or_none()
    if res is None:
        raise BucketDoesNotExistException(bucket_uuid)
    return res

def check_user_resource_access(resource: S3Resources, user : Users,
                                      allow_public : bool = True,
                                      needs_bucket_create_permission : bool = False,
                                      needs_add_user_permission : bool = False) -> bool:
    if allow_public is False and resource.public is True:
        raise ResourceCannotBeAccessedException(resource.resource_uuid, user.username)
    
    if user.user_type == UserType.superuser or resource.public is True:
        return True
        
    for permission in resource.permissions:
        if permission.user_id == user.id:
            if needs_bucket_create_permission and permission.can_create_buckets:
                return True
            if needs_add_user_permission and permission.can_add_users:
                return True
            if not needs_bucket_create_permission and not needs_add_user_permission:
                return True
            raise InsufficientPermissionsError
    
    raise ResourceCannotBeAccessedException(resource.resource_uuid, user.username)


def check_user_has_access_to_bucket(bucket_uuid: uuid.UUID, username : str, session : Session) -> bool:
    user = _get_user_raw(username, session)
    
    if user.user_type == UserType.superuser:
        return True
    
    stmt = select(S3Buckets.id).where(S3Buckets.bucket_uuid == bucket_uuid)
    stmt = stmt.join(S3Buckets.permissions).where(S3BucketPermissions.user_id == user.id)
    
    if session.execute(stmt).scalar_one_or_none() is None:
        raise ResourceCannotBeAccessedException(bucket_uuid, username)
    return True