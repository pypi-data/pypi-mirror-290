from etiket.exceptions.exceptions import FileNotAvailableException
from etiket.db.data_models.file import _FileCreate, FileRead, _FileUpdate, FileSelect
from etiket.db.models import Files, Datasets

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from etiket.db.data_access_objects.base import dao_base
from etiket.db.data_access_objects.dataset import _get_ds_by_uuid

from typing import Optional, List
from uuid import UUID

import datetime

class dao_File(dao_base):
    @staticmethod
    def create(fileCreate : _FileCreate, session : Session):
        ds = _get_ds_by_uuid(fileCreate.ds_uuid, None ,session)
        file = Files(**fileCreate.model_dump(by_alias=True, exclude=["ds_uuid"]),
                      scope_id=ds.scope.id, dataset_id=ds.id, bucket_id=ds.scope.bucket_id)
        ds.files.append(file)
        ds.modified = datetime.datetime.now(tz=datetime.timezone.utc)
        session.commit()
        return file
        
    @staticmethod
    def read(fileSelect : FileSelect, session : Session):
        files = _get_File_raw(fileSelect.uuid, fileSelect.version_id, session)
        return [FileRead.model_validate(file) for file in files]
    
    @staticmethod
    def read_by_name(datasetUUID : UUID, name : str, session : Session):
        stmt = select(Files).join(Datasets).where(Files.name == name).where(Datasets.uuid == datasetUUID)
        files = session.execute(stmt).scalars().all()
        return [FileRead.model_validate(file) for file in files]
    
    @staticmethod
    def read_raw(file_uuid : UUID, version_id : int, session : Session) -> Files:
        return _get_File_raw(file_uuid, version_id, session)[0]
        
    @staticmethod
    def update(fileUpdate : _FileUpdate, session : Session):
        file = _get_File_raw(fileUpdate.uuid, fileUpdate.version_id, session)[0]
        dao_File._update(file, fileUpdate, session)


    @staticmethod
    def delete(fileSelect : FileSelect, session : Session):
        files = _get_File_raw(fileSelect.uuid, fileSelect.version_id, session)
        for file in files:
            session.delete(file)
        session.commit()

def _get_File_raw(file_uuid : UUID, version_id : Optional[int], session : Session) -> List[Files]:
    try:
        stmt = select(Files).where(Files.uuid == file_uuid)
        if version_id:
            stmt = stmt.where(Files.version_id == version_id)
        files =  session.execute(stmt).scalars().all()
        if not files : 
            raise FileNotAvailableException
        return files
    except:
        raise FileNotAvailableException