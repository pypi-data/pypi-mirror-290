import uuid 

from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

from etiket.db.types import ObjectStoreType, S3ScopeTransferStatus
from etiket.db.data_models.scope import ScopeRead
from etiket.db.data_models.user import UserRead
class S3ResourcePermission(BaseModel):
    can_create_buckets : bool
    can_add_users : bool

class S3ResourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    type : ObjectStoreType
    
    resource_uuid : uuid.UUID
    endpoint : str
    region : Optional[str] = Field(None)
    access_key : str
    
    created_by : UserRead
    
    public : Optional[bool] = Field(False)
    permissions: S3ResourcePermission
    
    @field_validator('permissions',  mode='before')
    @classmethod
    def validate_permissions_before(cls, permission):
        if len(permission) == 0:
            return S3ResourcePermission(can_create_buckets=False, can_add_users=False)
        return S3ResourcePermission(can_create_buckets=permission[0].can_create_buckets,
                                    can_add_users=permission[0].can_add_users)

    def model_post_init(self, __context):
        if self.public is True:
            self.permissions = S3ResourcePermission(can_create_buckets=True, can_add_users=False)
        return self

class S3BucketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name : str
    bucket_uuid : uuid.UUID
    
    resource : S3ResourceRead    
    
class S3ResourceCreate(BaseModel):
    name: str = Field(min_length=5, max_length=100)
    type : ObjectStoreType
    
    endpoint : str
    region : Optional[str] = Field(None)
    
    access_key : str
    secret_key : str
    
    public : Optional[bool] = Field(False)

class S3ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    access_key : Optional[str] = Field(None)
    secret_key : Optional[str] = Field(None)

class S3TransferStatus(BaseModel):
    scope_transfer_id : int
    scope : ScopeRead
    bucket : S3BucketRead
    status : S3ScopeTransferStatus
    bytes_transferred : int
    total_bytes : int
