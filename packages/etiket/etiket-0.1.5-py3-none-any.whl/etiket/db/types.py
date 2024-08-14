from pydantic import StringConstraints
from typing import Annotated

import enum

class TokenType(enum.StrEnum):
    access   = "access"
    refresh  = "refresh"
    
class UserType(enum.StrEnum):
    admin = "admin"
    scope_admin  = "scope_admin"
    standard_user = "standard_user"
    superuser = "superuser"

class FileType(enum.StrEnum):
    HDF5 = "HDF5"
    HDF5_NETCDF = "HDF5_NETCDF"
    NDARRAY = "NDARRAY"
    JSON = "JSON"
    TEXT = "TEXT"
    UNKNOWN = "UNKNOWN"

class FileStatus(enum.StrEnum):
    announced = "announced"
    pending = "pending"
    secured = "secured"

class UploadConcat(enum.StrEnum):
    partial = "partial"
    final = "final"

class SoftwareType(enum.StrEnum):
    etiket = "etiket"
    dataQruiser = "dataQruiser"
    qdrive = "qdrive"

class UserLogStatus(enum.StrEnum):
    pending = "pending"
    secured = "secured"
    
class ObjectStoreType(enum.StrEnum):
    TUD = "TUD"
    AWS = "AWS"
    AZURE = "AZURE"
    SWIFT = "SWIFT"

class S3ScopeTransferStatus(enum.StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class S3FileTransferStatus(enum.StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

namestr     = Annotated[str, StringConstraints(min_length=1, max_length=100)]
usernamestr = Annotated[str, StringConstraints(min_length=4, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")]
metastr     = Annotated[str, StringConstraints(min_length=1, max_length=255)]
filestr     = Annotated[str, StringConstraints(min_length=2, max_length=255)]
datasetstr  = Annotated[str, StringConstraints(min_length=2, max_length=255)]
collectionstr = Annotated[str, StringConstraints(min_length=2, max_length=255)]
uidstr      = Annotated[str, StringConstraints(min_length=5, max_length=80)]
scopestr    = Annotated[str, StringConstraints(min_length=4, max_length=100,  pattern=r"^[a-zA-Z0-9_ -]+$")]
passwordstr = Annotated[str, StringConstraints(min_length=6, max_length=20)]