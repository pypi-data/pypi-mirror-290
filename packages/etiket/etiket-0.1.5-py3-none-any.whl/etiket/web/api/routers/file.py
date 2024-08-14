from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_scope_admin, is_admin, is_admin_type

from fastapi import APIRouter, Depends, status

from etiket.db.data_access_objects.file import dao_File
from etiket.db.data_models.file import FileCreate, _FileUpdate, _FileCreate, FileStatus,\
                                        FileSignedUploadLinks, FileValidate, FileRead, FileSelect,\
                                        FileSignedUploadLink

from etiket.db.data_models.token import AccessToken

from etiket.storage.S3_upload import S3Upload
from etiket.storage.S3_keygen import generate_key

from etiket.settings import settings
from etiket.exceptions.exceptions import FileIsImmutableException, FileAlreadyUploadedException

from typing import List, Optional
import uuid

router = APIRouter(tags=["files"])

# TODO check access of user to the dataset.
@router.post("/file/", status_code=status.HTTP_201_CREATED)
def add_file(*, fileCreate: FileCreate,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    key = generate_key(fileCreate.uuid, fileCreate.version_id)
    file = _FileCreate(**fileCreate.model_dump(), etag=None,
                       status=FileStatus.announced, s3_key=key)
    dao_File.create(file, session)

@router.get("/file/presigned_link/", response_model=FileSignedUploadLinks)
def get_presigned_link_multi(*, file_uuid : uuid.UUID,
                        version_id : int,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    # note currently any file can be replaced by this function TODO restrict THIS!
    file = dao_File.read_raw(file_uuid, version_id, session=session)
    if file.immutable and file.etag is not None:
        return FileIsImmutableException
    
    if file.upload_id:
        try:
            S3Upload.abort(file.bucket_id, generate_key(file.uuid,file.version_id), file.upload_id)
        except:
            pass

    upload_id, presigned_urls = S3Upload.create_multi(file.bucket_id, file.s3_key, file.size)
    dao_File.update(_FileUpdate(uuid=file.uuid,version_id=file.version_id, status=FileStatus.pending, upload_id=upload_id), session=session)
    return FileSignedUploadLinks(uuid=file_uuid, version_id=version_id, upload_id=upload_id, presigned_urls=presigned_urls)

@router.get("/file/presigned_link/single_part/", response_model=FileSignedUploadLink)
def get_presigned_link_single(*, file_uuid : uuid.UUID,
                        version_id : int,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    # note currently any file can be replaced by this function TODO restrict THIS!
    file = dao_File.read_raw(file_uuid, version_id, session=session)
    if file.immutable and file.etag is not None:
        return FileIsImmutableException
     
    url = S3Upload.create_single(file.bucket_id, file.s3_key, file.size)
    dao_File.update(_FileUpdate(uuid=file.uuid,version_id=file.version_id, status=FileStatus.pending), session=session)
    return FileSignedUploadLink(uuid=file_uuid, version_id=version_id, url= url)


@router.post("/file/validate_upload/", status_code=status.HTTP_202_ACCEPTED)
def validate_upload(*, fileValidate : FileValidate,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    file = dao_File.read_raw(fileValidate.uuid, fileValidate.version_id, session=session)
    if file.immutable and file.etag is not None:
        return FileIsImmutableException
    
    etag = S3Upload.complete(file.bucket_id, generate_key(fileValidate.uuid, fileValidate.version_id), fileValidate.upload_id, fileValidate.etags)
    file_update = _FileUpdate(uuid=fileValidate.uuid, version_id=fileValidate.version_id,
                              md5_checksum=fileValidate.md5_checksum,
                              etag=etag, status=FileStatus.secured, upload_id='')
    dao_File.update(file_update, session)

@router.post("/file/validate_upload/single_part/", status_code=status.HTTP_202_ACCEPTED)
def validate_upload_single(*, fileValidate : FileValidate,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    file = dao_File.read_raw(fileValidate.uuid, fileValidate.version_id, session=session)
    if file.immutable and file.etag is not None:
        return FileIsImmutableException
    
    file_update = _FileUpdate(uuid=fileValidate.uuid, version_id=fileValidate.version_id,
                              md5_checksum=fileValidate.md5_checksum,
                              etag=fileValidate.md5_checksum, status=FileStatus.secured, upload_id='')
    dao_File.update(file_update, session)

# TODO add read_files?
@router.get("/file/", response_model=List[FileRead])
def read_file(*, fileSelect : FileSelect,
                 accessToken: AccessToken = Depends(is_any),
                 session: Session = Depends(get_db_session) ):
    # TODO secure that you can only get a file where you have access to
    return dao_File.read(fileSelect, session=session)

@router.get("/file/by_name/", response_model=List[FileRead])
def read_file_by_name(*, dataset_uuid, name : str,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    return dao_File.read_by_name(dataset_uuid, name, session=session)

@router.post("/file/mark_immutable/", status_code=status.HTTP_202_ACCEPTED)
def mark_immutable(file_uuid, version_id, session):
    dao_File.update(_FileUpdate(uuid=file_uuid, version_id=version_id, immutable=True), session=session)

@router.delete("/file/", status_code=status.HTTP_200_OK)
def delete_file(*, file_uuid = uuid.UUID,
                            accessToken: AccessToken = Depends(is_admin),
                            session: Session = Depends(get_db_session) ):
    fileSelect = FileSelect(uuid = file_uuid, version_id=None) 
    dao_File.delete(fileSelect, session)