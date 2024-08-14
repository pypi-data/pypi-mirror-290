import datetime, uuid

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer

from etiket.db.types import FileType, FileStatus
from etiket.storage.S3_download import S3Download
from etiket.storage.S3_keygen import generate_key
from etiket.settings import settings

class FileBase(BaseModel):
    name : str
    uuid : uuid.UUID
    filename : str
    immutable : bool
    file_generator : str
    version_id : int
    creator : str
    collected : datetime.datetime
    size : int
    type : FileType

class FileCreate(FileBase):
    ds_uuid : uuid.UUID

class _FileCreate(FileCreate):
    etag: Optional[str] = Field(default=None)
    size : int
    status : FileStatus
    s3_key : str

class FileRead(FileBase):
    model_config = ConfigDict(from_attributes=True)

    created: datetime.datetime
    modified: datetime.datetime
    md5_checksum : Optional[str]
    etag: Optional[str]
    status : FileStatus
    
    S3_link : Optional[str] = Field(default=None)
    # making this alias is a little bit dirty, but the easiest way to put it in the object with it.
    S3_validity : Optional[float] = Field(default=None, validation_alias='bucket_id') # POSIX time

    def model_post_init(self, __context):
        if self.status == FileStatus.secured:
            key = generate_key(self.uuid, self.version_id)
            bucket_id = int(self.S3_validity)
            self.S3_link, self.S3_validity = S3Download.get_url(bucket_id, key, self.filename)        

    @field_validator('md5_checksum', mode='before')
    @classmethod
    def convert_orm_type_to_hash(cls, md5_checksum : uuid.UUID):
        if md5_checksum is not None:
            return md5_checksum.hex
        return None

class _FileUpdate(BaseModel):
    uuid : uuid.UUID
    version_id : int
    
    immutable : Optional[bool] = Field(default=None)
    md5_checksum : Optional[str] = Field(default=None)
    etag: Optional[str] = Field(default=None)
    status : Optional[FileStatus] = Field(default=None)
    upload_id : Optional[str] = Field(default=None)
 
   
    @field_serializer('md5_checksum')
    def serialize_dt(self, md5_checksum: str, _info):
        return uuid.UUID(md5_checksum)
    
class FileDelete(BaseModel):
    uuid : uuid.UUID
    
class FileSelect(BaseModel):
    uuid : uuid.UUID
    version_id : Optional[int] = Field(default=None) 

class FileSignedUploadLinks(BaseModel):
    uuid : uuid.UUID
    version_id : int
    upload_id : str
    part_size : int = Field(default=settings.S3_MULTIPART_UPLOAD_PARTSIZE)
    presigned_urls : List[str]

class FileSignedUploadLink(BaseModel):
    uuid : uuid.UUID
    version_id : int
    url : str

class FileValidate(BaseModel):
    uuid : uuid.UUID
    version_id : int
    upload_id : str
    md5_checksum : str
    etags: Optional[List[str]] = Field(default=None)   #this should be required when asking to validate otherwise one gets internal server error if 

