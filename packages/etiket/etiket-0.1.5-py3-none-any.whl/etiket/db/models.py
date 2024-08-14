from typing import List, Optional

from sqlalchemy import ForeignKey, UniqueConstraint, func, Index, text, literal_column
from sqlalchemy.orm import Mapped, mapped_column,\
                            DeclarativeBase, relationship
from sqlalchemy.types import JSON, BigInteger, DateTime

from etiket.db.types import FileStatus, FileType, UserType, SoftwareType, UserLogStatus, ObjectStoreType, S3ScopeTransferStatus, S3FileTransferStatus

from uuid import UUID
from datetime import datetime

# needed for unit tests as sqlalchemy does not map to bigint's (fails at autoincrementing the primary index)
from sqlalchemy.dialects import postgresql, sqlite

BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(postgresql.BIGINT(), 'postgresql')
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), 'sqlite')

class Base(DeclarativeBase):
    pass

class ScopeUserLink(Base):
    __tablename__ = "scope_user_link"
    scope: Mapped[int] = mapped_column(ForeignKey("scopes.id"), primary_key=True) 
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True) 

class Scopes(Base):
    __tablename__ = "scopes"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True)
    created : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    name : Mapped[str]
    description : Mapped[str]
    archived : Mapped[bool] = mapped_column(default=False)
    schema_id : Mapped[Optional[int]] = mapped_column(ForeignKey("schemas.id"))
    bucket_id : Mapped[int] = mapped_column(ForeignKey("s3_buckets.id"))
    
    schema : Mapped["Schemas"] = relationship(back_populates="scopes")
    users : Mapped[List["Users"]] = relationship(back_populates="scopes", secondary="scope_user_link")
    bucket : Mapped["S3Buckets"] = relationship(back_populates="scopes")

class Schemas(Base):
    __tablename__ = "schemas"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(unique=True)
    name : Mapped[str]
    description : Mapped[str]
    created : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    schema : Mapped[dict] = mapped_column(JSON)
    
    scopes : Mapped[List["Scopes"]] = relationship(back_populates="schema")

# TODO: I think we should make a SchAttribute table and schema should have a 1 to many relationship to it  

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    active: Mapped[bool] = mapped_column(default=True)
    disable_on: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    user_type: Mapped[UserType] 

    scopes: Mapped[List["Scopes"]] = relationship(back_populates="users", secondary="scope_user_link")

class Tokens(Base):
    __tablename__ = "tokens"
    session_id: Mapped[int] = mapped_column(primary_key=True)
    token_id: Mapped[int] = mapped_column()
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id")) 

class DsAttrLink(Base):
    __tablename__ = "ds_attr_link"
    
    dataset_id : Mapped[int] = mapped_column(ForeignKey("datasets.id"), primary_key=True) 
    dataset_attr_id : Mapped[int] = mapped_column(ForeignKey("dataset_attr.id"), primary_key=True) 
    
class Datasets(Base):
    __tablename__ = "datasets"
    __table_args__ = (
        UniqueConstraint('uuid', name = 'datasets_uuid_unique'), 
        UniqueConstraint('alt_uid', 'scope_id', name = 'datasets_alt_uid_scope_id_unique'), 
        Index('ix_search_helper_tsvector', func.to_tsvector(literal_column('simple'), text('search_helper')), postgresql_using='gin'), 
        #TODO 'simple' config has no stopwords and no stemming, is it better to use 'english', or shall I make both indexes and search in both?
    )
    id: Mapped[int] = mapped_column(BigIntegerType, primary_key=True)
    uuid : Mapped[UUID] = mapped_column(index=True)
    alt_uid : Mapped[Optional[str]] = mapped_column(index = True)
    collected: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    name: Mapped[str]
    scope_id : Mapped[int] = mapped_column(ForeignKey("scopes.id"), nullable=False, index=True)
    creator : Mapped[str]
    description : Mapped[Optional[str]]
    keywords : Mapped[List[str]] = mapped_column(JSON, nullable=False)
    notes : Mapped[Optional[str]]
    search_helper : Mapped[str]
    ranking : Mapped[int]

    scope : Mapped["Scopes"] = relationship(innerjoin=True)
    files : Mapped[List["Files"]] = relationship(cascade="all, delete")
    attributes  : Mapped[List["DatasetAttr"]] = relationship(secondary="ds_attr_link", back_populates="datasets")

class DatasetAttr(Base):
    __tablename__ = "dataset_attr"
    __table_args__ = (UniqueConstraint("key", "value", "scope_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    key : Mapped[str]
    value : Mapped[str]
    scope_id : Mapped[int] = mapped_column(ForeignKey("scopes.id"), index=True)
    
    datasets : Mapped[List[Datasets]] = relationship(secondary="ds_attr_link", back_populates="attributes")

class Files(Base):
    __tablename__ = "files"
    __table_args__ = (UniqueConstraint("uuid", "version_id"),)

    id: Mapped[int] = mapped_column(BigIntegerType, primary_key=True)
    name : Mapped[str]
    filename : Mapped[str]
    file_generator : Mapped[str]
    
    uuid : Mapped[UUID]
    creator : Mapped[str]
    type : Mapped[FileType]
    
    scope_id : Mapped[int] = mapped_column(ForeignKey("scopes.id"))
    dataset_id : Mapped[int] = mapped_column(ForeignKey("datasets.id"))

    collected: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    md5_checksum : Mapped[Optional[UUID]] # MD5 is just like a uuid 128 bits
    created : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified : Mapped[datetime]= mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    immutable : Mapped[bool] = mapped_column(default=True)
    
    etag: Mapped[Optional[str]] = mapped_column(default=None)
    size :  Mapped[int] = mapped_column(BigIntegerType)
    status : Mapped[FileStatus]
    version_id : Mapped[int] = mapped_column(BigIntegerType)
    bucket_id : Mapped[int] = mapped_column(ForeignKey("s3_buckets.id"))
    s3_key : Mapped[str] = mapped_column()
    upload_id : Mapped[Optional[str]]
    
    scope : Mapped["Scopes"] = relationship()

class software_versions(Base):
    __tablename__ = "software_versions"
    __table_args__ = (UniqueConstraint("type", "version", name = 'software_versions_type_version_unique'),)
    
    id : Mapped[int] = mapped_column(primary_key=True)
    type : Mapped[SoftwareType]
    version : Mapped[str]
    version_release_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    version_notes : Mapped[str]
    version_url : Mapped[str]
    needs_update : Mapped[bool] = mapped_column(default=False)

class software_releases(Base):
    __tablename__ = "software_releases"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    release_date : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    
    beta_release : Mapped[bool] = mapped_column(default=False)
    
    etiket_version_id : Mapped[int] = mapped_column(ForeignKey("software_versions.id"))
    qdrive_version_id : Mapped[int] = mapped_column(ForeignKey("software_versions.id"))
    dataQruiser_version_id : Mapped[int] = mapped_column(ForeignKey("software_versions.id"))
    
    min_etiket_version_id : Mapped[int] = mapped_column(ForeignKey("software_versions.id"))
    min_qdrive_version_id : Mapped[int] = mapped_column(ForeignKey("software_versions.id"))
    min_dataQruiser_version_id : Mapped[int] = mapped_column(ForeignKey("software_versions.id"))

    etiket_version : Mapped["software_versions"] = relationship(primaryjoin="software_releases.etiket_version_id == software_versions.id")
    dataQruiser_version : Mapped["software_versions"] = relationship(primaryjoin="software_releases.dataQruiser_version_id == software_versions.id")
    qdrive_version : Mapped["software_versions"] = relationship(primaryjoin="software_releases.qdrive_version_id == software_versions.id")
    
    min_etiket_version : Mapped["software_versions"] = relationship(primaryjoin="software_releases.min_etiket_version_id == software_versions.id")
    min_dataQruiser_version : Mapped["software_versions"] = relationship(primaryjoin="software_releases.min_dataQruiser_version_id == software_versions.id")
    min_qdrive_version : Mapped["software_versions"] = relationship(primaryjoin="software_releases.min_qdrive_version_id == software_versions.id")
    
class userLogs(Base):
    __tablename__ = "user_logs"
    
    id : Mapped[int] = mapped_column(primary_key=True)

    key : Mapped[str] = mapped_column(unique=True)
    reason : Mapped[Optional[str]]

    status : Mapped[UserLogStatus]
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    created : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    user : Mapped["Users"] = relationship(innerjoin=True)
 
class S3Resources(Base):
    __tablename__ = "s3_resources"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    
    name : Mapped[str]
    resource_uuid : Mapped[UUID] = mapped_column(unique=True)
    type : Mapped[ObjectStoreType]
    endpoint : Mapped[str]
    access_key : Mapped[str]
    secret_key : Mapped[str]
    region : Mapped[Optional[str]] = mapped_column(default=None)
    
    # public resource, i.e. resource that can be used for everyone! (this can only be added by superusers)
    public : Mapped[bool] = mapped_column(default=False)
    created_by_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
        
    buckets : Mapped[List["S3Buckets"]] = relationship(back_populates="resource")
    permissions : Mapped[List["S3ResourcePermissions"]] = relationship(back_populates="resource")
    created_by : Mapped["Users"] = relationship()

class S3ResourcePermissions(Base):
    __tablename__ = "s3_resource_permissions"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    
    resource_id = mapped_column(ForeignKey("s3_resources.id"))
    user_id = mapped_column(ForeignKey("users.id"))
    
    can_create_buckets : Mapped[bool] = mapped_column(default=True)
    can_add_users : Mapped[bool] = mapped_column(default=True)
    
    resource : Mapped["S3Resources"] = relationship(back_populates="permissions")
    user : Mapped["Users"] = relationship()
    
class S3Buckets(Base):
    __tablename__ = "s3_buckets"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    bucket_uuid : Mapped[UUID] = mapped_column(unique=True)
    name : Mapped[str]
    # other properties like bucket versioning, encryption, etc. can be added here
    resource_id : Mapped[int] = mapped_column(ForeignKey("s3_resources.id"))
    created_by_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    scopes : Mapped[List["Scopes"]] = relationship(back_populates="bucket")
    resource : Mapped["S3Resources"] = relationship(back_populates="buckets")
    permissions : Mapped[List["S3BucketPermissions"]] = relationship(back_populates="bucket")
    created_by : Mapped["Users"] = relationship()

class S3BucketPermissions(Base):
    __tablename__ = "s3_bucket_permissions"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    
    bucket_id : Mapped[int] = mapped_column(ForeignKey("s3_buckets.id"))
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    bucket : Mapped["S3Buckets"] = relationship(back_populates="permissions")
    user : Mapped["Users"] = relationship()

class S3ScopeTransferOverview(Base):
    __tablename__ = "s3_transfer_overview_scope_level"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    
    scope_id : Mapped[int] = mapped_column(ForeignKey("scopes.id"))
    bucket_id : Mapped[int] = mapped_column(ForeignKey("s3_buckets.id"))
    
    bytes_transferred : Mapped[int] = mapped_column(BigIntegerType)
    bytes_total : Mapped[int] = mapped_column(BigIntegerType)
    
    delete_on_completion : Mapped[bool] = mapped_column(default=False)
    
    status : Mapped[S3ScopeTransferStatus]
    error_message : Mapped[Optional[str]]
    
    scope : Mapped["Scopes"] = relationship()
    bucket : Mapped["S3Buckets"] = relationship()
    transfers : Mapped[List["S3FileTransferOverview"]] = relationship(back_populates="transfer")

class S3FileTransferOverview(Base):
    __tablename__ = "s3_transfer_overview_file_level"
    __table_args__ = (Index("s3_file_transfers_index", "transfer_id", "attempts", "status"),)
    
    id : Mapped[int] = mapped_column(BigIntegerType, primary_key=True)
    
    transfer_id : Mapped[int] = mapped_column(ForeignKey("s3_transfer_overview_scope_level.id"))
    
    file_id : Mapped[int] = mapped_column(ForeignKey("files.id"))
    status : Mapped[S3FileTransferStatus] = mapped_column(default=S3FileTransferStatus.PENDING)
    attempts : Mapped[int] = mapped_column(default=0)
    
    file : Mapped["Files"] = relationship()
    transfer : Mapped["S3ScopeTransferOverview"] = relationship(back_populates="transfers")
    
    