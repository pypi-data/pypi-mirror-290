import boto3, re

from etiket.db.models import S3Resources
from etiket.db.types import ObjectStoreType
from etiket.exceptions.exceptions import S3FaultyEndpointException, S3NoRegionSpecifiedException,\
    S3ConnectionException, S3PermissionException, S3BucketAlreadyOwnedByYouException,\
    S3BucketAlreadyExistsException, S3BucketCreationException, S3BucketCheckFailedException,\
    S3InvalidBucketNameException, S3BucketDoesNotExistsException, S3Error


def test_resource(resource : S3Resources) -> None:
    if resource.type == ObjectStoreType.AWS:
        if not resource.endpoint.endswith("amazonaws.com"):
            raise S3FaultyEndpointException(resource.endpoint, "amazonaws.com", resource.type)
    if resource.type == ObjectStoreType.AZURE:
        if not resource.endpoint.endswith("blob.core.windows.net"):
            raise S3FaultyEndpointException(resource.endpoint, "blob.core.windows.net", resource.type)
        if not resource.endpoint.endswith("tudelft.nl"):
            raise S3FaultyEndpointException(resource.endpoint, "tudelft.nl", resource.type)
    if resource.type == ObjectStoreType.SWIFT:
        # currently only surfsara.nl is supported
        if not resource.endpoint.endswith("surfsara.nl"):
            raise S3FaultyEndpointException(resource.endpoint, "surfsara.nl", resource.type)
        
    if ((resource.region == "" or resource.region == None) and 
        resource.type in [ObjectStoreType.AWS, ObjectStoreType.AZURE]):
        raise S3NoRegionSpecifiedException(resource.type)
    
    try :
        S3_client_test = boto3.client( "s3", endpoint_url=resource.endpoint,
                                        use_ssl=True, verify=True,
                                        aws_access_key_id=resource.access_key,
                                        aws_secret_access_key=resource.secret_key,
                                        region_name=resource.region,
                                        )
        S3_client_test.list_buckets()
    except Exception as e:
        raise S3ConnectionException(resource.access_key, resource.endpoint, resource.region) from e

def validate_bucket_name(bucket_name : str): 
    if not re.match(r"(?!(^xn--|.+-s3alias$|.*--))^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", bucket_name):
        raise S3InvalidBucketNameException(bucket_name)
 
def create_bucket(resource : S3Resources, bucket_name : str):
    validate_bucket_name(bucket_name)    
    if resource.type in [ObjectStoreType.AWS, ObjectStoreType.SWIFT]:
        try:
            S3_client = boto3.client( "s3", endpoint_url=resource.endpoint,
                                  use_ssl=True, verify=True,
                                  aws_access_key_id=resource.access_key,
                                  aws_secret_access_key=resource.secret_key,
                                  region_name=resource.region,
                                  )
            S3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration={'LocationConstraint': resource.region})
        except S3_client.exceptions.BucketAlreadyOwnedByYou:
            raise S3BucketAlreadyOwnedByYouException(bucket_name)
        except S3_client.exceptions.BucketAlreadyExists:
            raise S3BucketAlreadyExistsException(bucket_name)
        except Exception as e:
            raise S3BucketCreationException(bucket_name) from e
    elif resource.type == ObjectStoreType.AZURE:
        raise S3Error("Azure bucket creation not implemented yet")
    else:
        raise S3Error(f"Bucket creation not implemented for {resource.type}")

def check_if_bucket_exists(resource : S3Resources, bucket_name : str):
    validate_bucket_name(bucket_name)

    if resource.type in [ObjectStoreType.AWS, ObjectStoreType.SWIFT, ObjectStoreType.TUD]:
        try:
            S3_client = boto3.client( "s3", endpoint_url=resource.endpoint,
                                  use_ssl=True, verify=True,
                                  aws_access_key_id=resource.access_key,
                                  aws_secret_access_key=resource.secret_key,
                                  region_name=resource.region,
                                  )
            response = S3_client.list_buckets()
            for bucket in response['Buckets']:
                if (bucket['Name'] == bucket_name and 
                    S3_client.get_bucket_location(Bucket=bucket['Name'])['LocationConstraint'] == resource.region):
                    return
        except Exception as e:
            raise S3BucketCheckFailedException(bucket_name) from e
        
        raise S3BucketDoesNotExistsException(bucket_name)
    elif resource.type == ObjectStoreType.AZURE:
        raise NotImplementedError("Azure bucket creation not implemented yet")
    else:
        raise NotImplementedError(f"Bucket creation not implemented for {resource.type}")