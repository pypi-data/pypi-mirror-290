from etiket.exceptions.exceptions import FailedToGenerateUploadLinks,\
    FailedToCompleteUpload, FailedToAbortUpload, UploadFailedException
from etiket.settings import settings
from etiket.storage.client import S3BucketMgr

import math, typing, botocore

# TODO test upload of larger files.
class S3Upload:
    @staticmethod
    def create_single(bucket_id : int, key : str, size : int) -> str:
        bucket_info = S3BucketMgr.get_bucket(bucket_id)
        url = bucket_info.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": bucket_info.name,
                    "Key": key},
            ExpiresIn=settings.S3_PRESIGN_EXPIRATION_UPLOAD)
        return url
    
    @staticmethod
    def create_multi(bucket_id : int, key: str, size : int) -> typing.Tuple[str, typing.List[str]]:
        try:
            bucket_info = S3BucketMgr.get_bucket(bucket_id)  
            res = bucket_info.client.create_multipart_upload(Bucket = settings.S3_BUCKET, Key=key)
            upload_id = res['UploadId']
            n_parts = math.ceil(size / settings.S3_MULTIPART_UPLOAD_PARTSIZE)
            if n_parts == 0: n_parts=1 #just in case user sets length to zero
            
            presigned_urls = []
            for i in range(n_parts):
                upload_url = bucket_info.client.generate_presigned_url(
                        'upload_part',
                        Params={'Bucket': bucket_info.name,
                                'Key': key,
                                'UploadId': res['UploadId'],
                                'PartNumber': i + 1,
                                # 'ContentLengthRange': f'0-{settings.S3_MULTIPART_UPLOAD_PARTSIZE}', #TODo this does not seem to exist
                                },
                        ExpiresIn=settings.S3_PRESIGN_EXPIRATION_UPLOAD) # 1 day should be sufficient for all uploads.
                presigned_urls.append(upload_url)
        except Exception as e:
            print(e)
            raise FailedToGenerateUploadLinks
        return upload_id, presigned_urls

    @staticmethod
    def complete(bucket_id : int, key : str, upload_id : str,  etags : typing.List[str]):
        try: 
            bucket_info = S3BucketMgr.get_bucket(bucket_id)  
            
            parts = [{'ETag': etags[i], 'PartNumber': i + 1} for i in range(len(etags))]

            res = bucket_info.client.complete_multipart_upload(
                Bucket=bucket_info.name,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={'Parts': parts})
            ETag = res['ETag']
        except Exception as e :
            print(e)
            raise FailedToCompleteUpload
        return ETag
    
    @staticmethod
    def abort(bucket_id : int, key : str, upload_id:str):
        try:
            bucket_info = S3BucketMgr.get_bucket(bucket_id)  
            res = bucket_info.client.abort_multipart_upload(
                Bucket=bucket_info.name, Key=key, UploadId=upload_id
            )
        except Exception:
            raise FailedToAbortUpload
        return res
    
    @staticmethod
    def check_upload_single_part(bucket_id : int, key : str) -> None:
        try:
            bucket_info = S3BucketMgr.get_bucket(bucket_id)  
            res = bucket_info.client.head_object(Bucket=bucket_info.name, Key=key)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise UploadFailedException("Object not found.")
            raise UploadFailedException(e)