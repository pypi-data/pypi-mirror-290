import os
os.chdir("../../../")

from etiket.settings import settings

settings.S3_ENDPOINT = "http://0.0.0.0:4566"
settings.S3_PREFIX = None 
settings.S3_ACCESS_KEY_ID = "test"
settings.S3_SECRET_ACCESS_KEY = "test"

from etiket.db.data_access_objects.schema import dao_schema
from etiket.db.get_db_session import SessionLocal

from etiket.db.data_models.file import  FileCreate, FileUpdate, FileRead, _FileCreate
from etiket.db.data_models.scope import ScopeUpdate, ScopeCreate, ScopeRead
from etiket.db.data_models.dataset import  DatasetCreate

from etiket.db.data_access_objects.scope import dao_scope
from etiket.db.data_access_objects.dataset import dao_dataset
from etiket.db.data_access_objects.file import dao_File

from etiket.storage.S3_download import S3Download
from etiket.storage.S3_upload import S3Upload

from moto import mock_s3

from uuid import uuid4
import unittest, boto3, requests, math

from datetime import datetime

chunk_size = 5242880

class test_file_stuff(unittest.TestCase):
    def setUp(self):
        # set-up with localstack to test S3
        s3 = boto3.client("s3", endpoint_url=settings.S3_ENDPOINT,
                            aws_access_key_id=settings.S3_ACCESS_KEY_ID ,
                            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
                            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
                            region_name=settings.S3_REGION_NAME,
                            )
        bucket = s3.create_bucket(Bucket=settings.S3_BUCKET)

    def uploadFile(self, file_name, presigned_urls):
        etags = []

        n_bytes = os.path.getsize(file_name)
        n_parts = math.ceil(n_bytes / chunk_size) #5MB

        for i in range(n_parts):
            with open(file_name, 'rb') as file:
                file.seek(i * chunk_size)
                data = file.read(chunk_size)
            response = requests.put(presigned_urls[i], data=data)
            etags.append(response.headers['ETag'])
        return etags
        
    def test_create_and_read_update_delete_of_single_files(self):
        with SessionLocal() as session:
            scope = _create_scope("name", session)
            dataset = _create_ds(scope, session)

            file_uuid = uuid4()
            fc = FileCreate(uuid=file_uuid, name  = "test", creator="anom",
                            collected=datetime.now(),
                            type=FileType.raw, version=0, ds_uuid = dataset.uuid)
            db_internal = _FileCreate(**fc.model_dump(), size=10, etag=None, status=FileStatus.pending, s3_bucket=settings.S3_BUCKET, s3_key=str(file_uuid))

            file = dao_File.create(scope.uuid, db_internal, session)
            session.commit()
            dataset.files.append(file)
            session.commit()
        
            file_info = dao_File.read(file_uuid, session)
            
            self.assertEqual(file_info.status, FileStatus.pending)
            self.assertEqual(file_info.nbytes, 10)
            self.assertEqual(file_info.etag, None)
            self.assertEqual(file_info.uuid, file_uuid)
            self.assertEqual(file_info.url, None)
            
            ETag = self._upload_test_file(file_uuid)
            fu = FileUpdate(etag=ETag, status=FileStatus.available)
            dao_File.update(file_uuid, fu, session)
            session.commit()
            
            file_info = dao_File.read(file_uuid, session)
            
            self.assertEqual(file_info.status, FileStatus.available)
            self.assertEqual(file_info.nbytes, 10)
            self.assertNotEqual(file_info.etag, None)
            self.assertNotEqual(file_info.url, None)
            
            # check if the file is in the the dataset when requested:
            ds_read = dao_dataset.read(dataset.uuid, None, session)

            self.assertEqual(ds_read.files[0].url, file_info.url)

            _delete_ds(dataset.uuid, session)        
            _delete_scope(scope.uuid, session)

    def _upload_test_file(self, file_uuid):
        self.setUp()

        f_name = 'testfile.txt'
        
        with open(f_name, 'w') as f:
            f.write('Create a new text file!')

        n_bytes = os.path.getsize(f_name)
        upload_id, presigned_urls = S3Upload.create(file_uuid, n_bytes)

        etags = self.uploadFile(f_name, presigned_urls)
        ETag = S3Upload.complete(file_uuid, upload_id, etags)
        # just for testing
        get_link = S3Download.get_url(file_uuid, f_name)
        return ETag

def _create_scope(name, session):
    create_obj = ScopeCreate(name = name, uuid=uuid4(), description="test-scope")
    dao_scope.create(create_obj, session)
    session.commit()
    return create_obj


def _delete_scope(scope_uuid, session):
    dao_scope.delete(scope_uuid, session)
    session.commit()

def _create_ds(scope, session, collected = datetime.now(), name = "test dataset"):
    datasetCreate1 = DatasetCreate(uuid = uuid4(), collected=collected, 
                        name = name, creator="Anonymous",
                        keywords=["vP1 (mV)", "RF readout signal (mV)"],
                        ranking=0, scope_uuid= scope.uuid,
                        attributes={})
    dataset = dao_dataset.create(datasetCreate1, session)
    session.commit()
    return dataset

def _delete_ds(dataset_uuid, session):
    dao_dataset.delete(dataset_uuid, session)
    session.commit()

if __name__ == '__main__':
    from etiket.db.get_db_session import SessionLocal, engine
    from etiket.db.models import *

    Base.metadata.create_all(engine)

    unittest.main()