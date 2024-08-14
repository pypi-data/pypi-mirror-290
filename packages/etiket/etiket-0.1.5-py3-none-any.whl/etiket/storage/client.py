from dataclasses import dataclass
from typing import Any, Dict

from etiket.settings import settings
from etiket.db.data_access_objects.S3_utility import get_bucket_by_id, get_resource_by_id
from etiket.db.get_db_session import get_db_session_raw

import boto3

@dataclass
class Bucket_info_raw:
    name: str
    resource_id: Any


@dataclass
class Bucket:
    name: str
    client: Any

# TODO auto check for changes in resource settings.
class S3ResourceMgr:
    _resources: Dict[int, Any] = {}

    @classmethod
    def get_client(cls, resource_id: int) -> Any:
        if resource_id not in cls._resources:
            cls._resources[resource_id] = cls._create_client(resource_id)
        return cls._resources[resource_id]

    @classmethod
    def _create_client(cls, resource_id: int) -> Any:
        if resource_id == settings.S3_LOG_REPORTS_BUCKET_ID:
            return boto3.client(
                "s3",
                endpoint_url=settings.S3_LOG_REPORTS_ENDPOINT,
                use_ssl=True,
                verify=True,
                aws_access_key_id=settings.S3_LOG_REPORTS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.S3_LOG_REPORTS_SECRET_ACCESS_KEY,
                region_name=settings.S3_LOG_REPORTS_REGION_NAME
            )
        else:
            resource = get_resource_by_id(resource_id, get_db_session_raw())
            return boto3.client(
                "s3",
                endpoint_url=resource.endpoint,
                use_ssl=True,
                verify=True,
                aws_access_key_id=resource.access_key,
                aws_secret_access_key=resource.secret_key,
                region_name=resource.region
            )
class S3BucketMgr:
    _bucketResources: Dict[int, Bucket_info_raw] = {}

    @classmethod
    def get_bucket(cls, bucket_id: int) -> Bucket:
        if bucket_id not in cls._bucketResources:
            if bucket_id == settings.S3_LOG_REPORTS_BUCKET_ID:
                cls._bucketResources[bucket_id] = Bucket_info_raw(settings.S3_LOG_REPORTS_BUCKET, -1)
            else:
                bucket = get_bucket_by_id(bucket_id, get_db_session_raw())
                cls._bucketResources[bucket_id] = Bucket_info_raw(bucket.name, bucket.resource_id)
        
        b_raw = cls._bucketResources[bucket_id]
        return Bucket(b_raw.name, S3ResourceMgr.get_client(b_raw.resource_id))
