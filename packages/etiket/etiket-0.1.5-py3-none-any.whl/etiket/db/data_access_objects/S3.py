import uuid, logging
from sqlalchemy import select, insert, text, func, update
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List

from etiket.db.data_access_objects.base import dao_base
from etiket.db.data_access_objects.scope import _get_scope_raw
from etiket.db.data_access_objects.user import _get_user_raw
from etiket.db.data_access_objects.S3_utility import (
    _get_resource_raw, _get_bucket_raw, check_user_resource_access,
    check_user_has_access_to_bucket
)
from etiket.exceptions.exceptions import (
    SuperUserException, GrantAccessError, RevokeAccessError,
    CannotGrantForGenericResourceException, UserAlreadyHasAccessError,
    CannotRevokeOwnAccessError, ResourceAlreadyExistsError, NothingToTransferException
)
from etiket.db.data_models.S3 import (
    S3ResourceCreate, S3ResourceUpdate,
    S3TransferStatus, S3ResourcePermission, S3ResourceRead, S3BucketRead
)
from etiket.db.data_models.scope import ScopeRead
from etiket.db.models import (
    S3Resources, S3ResourcePermissions, S3Buckets, Users,
    S3ScopeTransferOverview, S3FileTransferOverview, Files, Scopes, S3BucketPermissions
)
from etiket.db.types import UserType, S3FileTransferStatus, S3ScopeTransferStatus
from etiket.storage.S3_management import test_resource, create_bucket, check_if_bucket_exists

logger = logging.getLogger(__name__)

class dao_S3_resources(dao_base):
    @staticmethod
    def create(new_resource: S3ResourceCreate, username: str, session: Session):
        user = _get_user_raw(username, session)
        
        if user.user_type != UserType.superuser and new_resource.public:
            raise SuperUserException("Only superusers are allowed to create public resources")
        
        resources = dao_S3_resources.read(username, user.user_type, session)
        for resource in resources:
            if resource.endpoint == new_resource.endpoint and resource.access_key == new_resource.access_key:
                raise ResourceAlreadyExistsError(resource.resource_uuid)
        
        resource = S3Resources(**new_resource.model_dump(), resource_uuid=uuid.uuid4(), created_by_id=user.id)
        test_resource(resource)
        
        session.add(resource)
        session.flush()
        
        if not new_resource.public:
            resource.permissions.append(S3ResourcePermissions(
                user_id=user.id,
                resource_id=resource.id,
                can_create_buckets=True,
                can_add_users=True
            ))
        
        session.commit()
    
    @staticmethod
    def update(resource_uuid: uuid.UUID, updated_resource: S3ResourceUpdate, username: str, session: Session):
        try:
            resource = _get_resource_raw(resource_uuid, session, load_permissions=True)
            user = _get_user_raw(username, session)
            if user.user_type != UserType.superuser:
                check_user_resource_access(resource, _get_user_raw(username, session), allow_public = False)
            if updated_resource.access_key:
                resource.access_key = updated_resource.access_key
            if updated_resource.secret_key:
                resource.secret_key = updated_resource.secret_key
            if updated_resource.name:
                resource.name = updated_resource.name
            test_resource(resource)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
    @staticmethod
    def read(username : str, user_type : UserType, session : Session) -> List[S3ResourceRead]:
        stmt1 = select(S3Resources).options(joinedload(S3Resources.created_by), selectinload(S3Resources.permissions))
        stmt1 = stmt1.where(S3Resources.public == True)
        
        stmt2 = select(S3Resources).options(joinedload(S3Resources.created_by), joinedload(S3Resources.permissions))
        stmt2 = stmt2.where(S3Resources.public == False)
        if user_type != UserType.superuser:
            stmt2 = stmt2.join(S3Resources.permissions).join(S3ResourcePermissions.user)
            stmt2 = stmt2.where(Users.username == username)
        
        res = session.execute(stmt1).unique().scalars().all() +  session.execute(stmt2).unique().scalars().all()
        return [S3ResourceRead.model_validate(r) for r in res]
    
    @staticmethod
    def grant_access(target_username: str, resource_uuid : uuid.UUID, permissions: S3ResourcePermission, username : str, session : Session):
        
        target_user = _get_user_raw(target_username, session)
        if target_user.user_type not in [UserType.admin, UserType.scope_admin]:
            raise GrantAccessError(target_username)
        
        resource = _get_resource_raw(resource_uuid, session, load_permissions = True)
        check_user_resource_access(resource, _get_user_raw(username, session), allow_public = False, needs_add_user_permission=True)
        
        if resource.public:
            raise CannotGrantForGenericResourceException()

        for permission in resource.permissions:
            if permission.user_id == target_user.id:
                raise UserAlreadyHasAccessError(target_username, resource_uuid)

        resource.permissions.append(S3ResourcePermissions(user_id = target_user.id, **permissions.model_dump()))
        session.commit()
    
    @staticmethod
    def revoke_access(target_username: str, resource_uuid : uuid.UUID, username : str, session : Session):
        if target_username == username:
            raise CannotRevokeOwnAccessError()
        
        target_user = _get_user_raw(target_username, session)
        resource = _get_resource_raw(resource_uuid, session, load_permissions=True)
        check_user_resource_access(resource, _get_user_raw(username, session), allow_public = False, needs_add_user_permission=True)
        
        stmt = select(S3ResourcePermissions).where(S3ResourcePermissions.user_id == target_user.id, S3ResourcePermissions.resource_id == resource.id)
        permission = session.execute(stmt).scalar_one_or_none()
        if permission is None:
            raise RevokeAccessError(username, resource_uuid)
        
        session.delete(permission)
        session.commit()

class dao_S3_buckets(dao_base):    
    @staticmethod
    def create(resource_uuid: uuid.UUID, bucket_name: str, username: str, session: Session):
        try:            
            resource = _get_resource_raw(resource_uuid, session, load_permissions=True)
            user = _get_user_raw(username, session)
            check_user_resource_access(resource, user, needs_bucket_create_permission=True)
            
            create_bucket(resource, bucket_name)
            
            new_bucket = S3Buckets(name=bucket_name, bucket_uuid=uuid.uuid4(), created_by_id=user.id)
            resource.buckets.append(new_bucket)
            
            if resource.public:
                new_bucket.permissions.append(S3BucketPermissions(user_id=user.id))
            else:
                user_ids = [permission.user_id for permission in resource.permissions]
                for user_id in user_ids:
                    new_bucket.permissions.append(S3BucketPermissions(user_id=user_id))
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
    @staticmethod
    def add_existing(resource_uuid: uuid.UUID, bucket_name: str, username: str, session: Session):
        try:            
            resource = _get_resource_raw(resource_uuid, session)
            user = _get_user_raw(username, session)
            check_user_resource_access(resource,user, needs_bucket_create_permission=True)
            check_if_bucket_exists(resource, bucket_name)
            
            new_bucket = S3Buckets(name=bucket_name, bucket_uuid=uuid.uuid4(), created_by_id=user.id)
            resource.buckets.append(new_bucket)
            
            user_ids = [permission.user_id for permission in resource.permissions]
            for user_id in user_ids:
                new_bucket.permissions.append(S3BucketPermissions(user_id=user_id))
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
    @staticmethod
    def read(username : str, user_type : UserType, session : Session) -> List[S3BucketRead]:
        stmt = select(S3Buckets).options(selectinload(S3Buckets.resource))#.options(selectinload(S3Resources.created_by)).options(selectinload(S3Resources.permissions))
        if user_type != UserType.superuser:
            stmt = stmt.join(S3Buckets.permissions).join(S3BucketPermissions.user).where(Users.username == username)

        res = session.execute(stmt).unique().scalars().all()
        return [S3BucketRead.model_validate(r) for r in res]
    
    @staticmethod
    def grant_access(new_user: str, bucket_uuid : uuid.UUID, username : str, session : Session):
        check_user_has_access_to_bucket(bucket_uuid, username, session)
        
        user = _get_user_raw(new_user, session)
        bucket = _get_bucket_raw(bucket_uuid, session, load_permissions = True)
        
        for permission in bucket.permissions:
            if permission.user_id == user.id:
                raise UserAlreadyHasAccessError(new_user, bucket_uuid)
        bucket.permissions.append(S3BucketPermissions(user_id = user.id))
        session.commit()
    
    @staticmethod
    def revoke_access(del_user : str, bucket_uuid : uuid.UUID, username : str, session : Session):
        check_user_has_access_to_bucket(bucket_uuid, username, session)
        
        user = _get_user_raw(del_user, session)
        bucket = _get_bucket_raw(bucket_uuid, session, load_permissions = True)
        
        stmt = select(S3BucketPermissions).where(S3BucketPermissions.user_id == user.id, S3BucketPermissions.bucket_id == bucket.id)
        permission = session.execute(stmt).scalar_one_or_none()
        if permission is None:
            raise RevokeAccessError(username, bucket_uuid)
        session.delete(permission)
        session.commit()

class dao_S3_transfers(dao_base):
    @staticmethod
    def transfer_data(scope_uuid: uuid.UUID, bucket_uuid: uuid.UUID, username : str, session : Session):
        try:
            check_user_has_access_to_bucket(bucket_uuid, username, session)

            bucket = _get_bucket_raw(bucket_uuid, session)       
            scope = _get_scope_raw(scope_uuid, session)
            scope.bucket = bucket
            
            # cancel any ongoing transfers
            stmt = select(S3ScopeTransferOverview).where(S3ScopeTransferOverview.scope_id == scope.id)
            stmt = stmt.where(S3ScopeTransferOverview.status.in_([S3ScopeTransferStatus.PENDING,
                                                                S3ScopeTransferStatus.IN_PROGRESS,]))
            for transfer in session.execute(stmt).scalars().all():
                transfer.status = S3FileTransferStatus.CANCELLED
            
            sub_query = select(S3ScopeTransferOverview.id).where(S3ScopeTransferOverview.scope_id == scope.id)
            stmt = update(S3FileTransferOverview).where(S3FileTransferOverview.transfer_id.in_(sub_query))
            stmt = stmt.where(S3FileTransferOverview.status==S3FileTransferStatus.PENDING)
            stmt = stmt.values(status=S3FileTransferStatus.CANCELLED)
            session.execute(stmt)
            
            # count how many files to transfer
            stmt = select(func.count(Files.id)).where(Files.scope_id == scope.id).where(Files.bucket_id != bucket.id)
            n_files =  session.execute(stmt).scalar_one()
            if n_files==0:
                raise NothingToTransferException()
            
            # add new transfer
            scope_transfer_overview = S3ScopeTransferOverview(scope_id = scope.id, bucket_id = bucket.id,
                                                    bytes_transferred = 0, bytes_total = 0, 
                                                    status = S3ScopeTransferStatus.PENDING)
            session.add(scope_transfer_overview)
            session.flush()
            
            # select files that need to be uploaded and calculate total size of the transfer
            select_stmt = select(Files.id, text(str(scope_transfer_overview.id)) ).where(Files.scope_id == scope.id)
            select_stmt = select_stmt.where(Files.bucket_id != bucket.id)
                    
            insert_stmt = insert(S3FileTransferOverview).from_select(["file_id", "transfer_id"], select_stmt)
            session.execute(insert_stmt)
            
            stmt = select(func.sum(Files.size)).where(Files.scope_id == scope.id).where(Files.bucket_id != bucket.id)
            scope_transfer_overview.bytes_total = session.execute(stmt).scalar_one()
            
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
    @staticmethod
    def status_overview(username : str, user_type : UserType, session : Session) -> List[S3TransferStatus]:
        stmt = select(S3ScopeTransferOverview).join(S3ScopeTransferOverview.scope).options(joinedload(S3ScopeTransferOverview.scope))
        stmt = stmt.options(joinedload(S3ScopeTransferOverview.bucket).joinedload(S3Buckets.resource))
        stmt = stmt.order_by(S3ScopeTransferOverview.id.desc())
        
        if user_type != UserType.superuser:
            stmt = stmt.join(Scopes.users).where(Users.username == username)
        res = session.execute(stmt).scalars().all()
        
        overview = []
        for r in res:
            scope = ScopeRead.model_validate(r.scope)
            bucket = S3BucketRead.model_validate(r.bucket)
            
            status = S3TransferStatus(scope_transfer_id=r.id,  scope = scope, bucket = bucket, status = r.status, 
                                        bytes_transferred = r.bytes_transferred, total_bytes = r.bytes_total)
            overview.append(status)
        
        return overview