import uuid
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from typing import Any, Dict, List

from etiket.db.types import ObjectStoreType

class BaseError(BaseModel):
    detail : str = Field(..., description="Error message or description")


class IncorrectUsernamePasswordException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE
        self.detail = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}


class ValidationCredentialsException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE
        self.detail = "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}

class InsufficientPrivigesException(HTTPException):
    def __init__(self, expected_type):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"Incorrect priviliges to acces this resource, you are expected to be a {expected_type}"

class UserIsNotOfAdminTypeException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"Incorrect priviliges to acces this resource, you are expected to be an admin or scope admin."
        
class InactiveUserException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Inactive user"

class AdminUserException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "User is not an admin"

class SuperUserException(HTTPException):
    def __init__(self, message = ""):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = message

class CannotCreateSuperUser(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "SuperUsers cannot be created via this interface."

class InvalidAccessTokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Access token is invalid"

class RefreshTokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could validate existing refresh token"

class TokenAbuseException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Token abuse detected. User has the relogin on all services."

class InvalidRefreshTokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not refresh token"

class TokenExpiredException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Access token is expired, please log in again or use a refresh token."

class AccessTokenExpectedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "A token with the type 'access' token was expected."

class RefreshTokenExpectedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "A token with the type 'refresh' token was expected."


class AccessTokenUsedAsRefreshTokenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Do not use access token to refresh"


class UserNotInScopeException(HTTPException):
    def __init__(self, scope):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"You are not part of scope {scope}"

class FileAlreadyExistsException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Filename already exists in dataset."

class MemberHasNoBusinessInThisScopeException(HTTPException):
    def __init__(self, scope_uuid):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"Can't access the scope with the uuid {scope_uuid}, since it (a) does not exist, (b) you don't have access to it."

class FileNotAvailableException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "File is not availabl.)"

class UnexpectedFileVersionException(HTTPException):
    def __init__(self, wanted_version, expected_version):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Expected file version is {expected_version} (received {wanted_version})."

class InvalidRangeException(HTTPException):
    def __init__(self, Range):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"Invalid request range (Range:{Range})"


class UserNotFoundException(HTTPException):
    def __init__(self, username: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = (f"User {username} not found",)


class UserAlreadyNotPartOfScopeException(HTTPException):
    def __init__(self, username: str, scope: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = (f"{username} is already not part of scope {scope}",)


class UserAlreadyPartOfScopeException(HTTPException):
    def __init__(self, username: str, scope: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = (f"{username} is already part of scope {scope}",)


class DatasetAlreadyPartOfCollectionException(HTTPException):
    def __init__(self, scope: str, dataset_uid, collection):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"Dataset {scope}/{dataset_uid} is already in collection"


class DatasetAlreadyNotPartOfCollectionException(HTTPException):
    def __init__(self, scope: str, dataset_uid, collection):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"Dataset {scope}/{dataset_uid} is already in collection"


class UploadStillInProgressException(HTTPException):
    def __init__(self, upload_uid):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"Upload at /uploads/{upload_uid} still in progress (maybe more)."


class NotAllUploadsCompletedYetException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Not all uploads are completed yet"


class IncompleteConcatUIDListException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "List of UIDs provided not complete"


class UploadGoneException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_410_GONE
        self.detail = "A part of the upload has been removed"

class UploadFailedException(HTTPException):
    def __init__(self, error_msg):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = f"Upload failed: {error_msg}"

class ChecksumMismatchException(HTTPException):
    def __init__(self):
        self.status_code = 460
        self.detail = "Checksum mismatch. Need to upload at this offset again"


class DownloadFailedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "Download failed. Contact system administrator"

class UploadTerminationFailedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "Termination upload failed, please try again"


class DatasetFileIsNonEmptyException(HTTPException):
    def __init__(self, scope, dataset_uid,name):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = f"{scope}/{dataset_uid} can not be deleted: non empty file {name}"

class FileIsImmutableException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "File is made immutable and already uploaded"

class FileAlreadyUploadedException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "File is already uploaded"

class FileIsNotEmptyException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "File is not empty and can not be deleted"


class NewVersionFileForbiddenException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "No new file version allowed"


class UnsupportedTusVersionException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Unsupported tus protocol version"


class UnsupportedChecksumAlgorithmException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Unsupported checksum algorithm"


class UnsupportedTusExtensionException(HTTPException):
    def __init__(self, extension: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Unsupported tus extension: no {extension}"


class UploadLengthException(HTTPException):
    def __init__(self, size: int):
        self.status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        self.detail = f"Upload length for (partial) upload larger than {size}"


class UploadOffsetMismatchException(HTTPException):
    def __init__(self, size: int):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "Offset of upload provided not the same as stored"


class UploadAlreadyCompletedException(HTTPException):
    def __init__(self, size: int):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = "Upload is already completed. Can not be continued"


class ContentTypeException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Content-Type needs to be application/offset+octet-stream"


class DeferUploadLengthException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "No upload length provided. Cannot be deffered."


class ContentLengthLargerThanUploadLengthException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Provided content length larger than provided upload length"


class UploadChecksumHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Incorrect Upload-Checksum header"


class UploadUUIDInConcatHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Not a valid upload UUID in Upload-Concat final header"


class UploadConcatHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Something went wrong while parsing Upload-Concat final header"


class UploadLengthInFinalConcatHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Upload length defined for final request for concatenation"


class UploadMetadataHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Invalid Upload-Metadata header"


class MissingScopeUploadMetadataHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "No scope defined in Upload-Metadata"


class MissingFileUIDUploadMetadataHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "No file UID defined in Upload-Metadata"


class InvalidFileUIDUploadMetadataHeaderException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Not a valid file UID in Upload-Metadata"

class SchemaDoesNotExistException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "The UUID does not refer to an existing Schema."

class SchemaDoesAlreadyExistException(HTTPException):
    def __init__(self, uuid):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot create a schema with the UUID ({uuid}), it already exists."

class SchemaNotValidException(HTTPException):
    def __init__(self, error_msg):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot create or update a schema, {error_msg}."

class ScopeDoesNotExistException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "The UUID does not refer to an existing Scope."
        
class ScopeDoesAlreadyExistException(HTTPException):
    def __init__(self, uuid):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot create a scope of an UUID ({uuid}) that already exists."



class CannotDeleteAScopeWithDatasetsException(HTTPException):
    def __init__(self, name):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot delete scope with the name ({name}) as it already contains datasets."

class UserDisabledException(HTTPException):
     def __init__(self, username: str):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = (f"User with {username} is disabled. Contact your administrator.")
        
class UserAlreadyExistsException(HTTPException):
    def __init__(self, username: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = (f"User with the username '{username}' already exists")

class UserMailAlreadyRegisteredException(HTTPException):
    def __init__(self, mail:str,):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = (f"The mail addres '{mail}' is already registered to another account")

class UserDoesNotExistException(HTTPException):
    def __init__(self, name:str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"User named '{name}' does not exist."

class SchemaAlreadyAssignedException(HTTPException):
    def __init__(self, schema:str, scope : str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"The schema '{schema}' is already assigned to the scope named '{scope}'"
        
class DatasetAlreadyExistException(HTTPException):
    def __init__(self, uuid):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot create a dataset with the UUID ({uuid}), it already exists."

class DatasetAltUIDAlreadyExistException(HTTPException):
    def __init__(self, uid):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot create a dataset with the UID ({uid}), it already exists."

class DatasetNotFoundException(HTTPException):
    def __init__(self, uuid):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Cannot find a dataset the given UUID ({uuid})."
class DatasetNotFoundExceptionUID(HTTPException):
    def __init__(self, uid):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Cannot find a dataset the given alt UID ({uid})."

class DatasetNotFoundExceptionUUIDAltUIDException(HTTPException):
    def __init__(self, id):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Cannot find a dataset the given UUID or alt UID -- id = {id}."

class DatasetPresentInMultipleScopesException(HTTPException):
    def __init__(self, datasets):
        self.status_code = status.HTTP_406_NOT_ACCEPTABLE
        self.detail = "Found the requested dataset  in multiple scopes. Please specify the scope : \n"
        for dataset in datasets:
            self.detail += f"\tScope: {dataset.scope.name} (UUID : {dataset.scope.uuid}) \n"

class DatasetCreateUIDUUIDException(HTTPException):
    def __init__(self, uuid, uid):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = f"Cannot create a dataset for which the UUID ({uuid}) and alternative uid ({uid}) are the same."
        
class CannotConnectToStorageBackEnd(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "Could not connect to the storage device",

class FailedToGenerateUploadLinks(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "Failed to create links for the multipart upload.",

class FailedToCompleteUpload(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "Could not complete the multipart upload.",
        
class FailedToAbortUpload(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "Could not abort the multipart upload.",
        
class FailedToCreateDownloadLink(HTTPException):
    def __init__(self, file_uuid):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = f"Failed to create download link for file with UUID f{file_uuid}",

class insufficientPrivilegesException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "Insufficient privileges to access this resource"

class UserLogNotFoundException(HTTPException):
    def __init__(self, key, username):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Could not find a log with the key {key}, for the user {username}"
        
        
class ResourceCannotBeAccessedException(HTTPException):
    def __init__(self, resource_uuid: uuid.UUID, username: str):
        detail = f"User '{username}' cannot access resource with UUID '{resource_uuid}'."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ResourceDoesNotExistException(HTTPException):
    def __init__(self, resource_uuid: uuid.UUID):
        detail = f"Resource with UUID '{resource_uuid}' does not exist."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BucketDoesNotExistException(HTTPException):
    def __init__(self, bucket_uuid: uuid.UUID):
        detail = f"Bucket with UUID '{bucket_uuid}' does not exist."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND , detail=detail)

class CannotAddBucketToGenericResourceException(HTTPException):
    def __init__(self):
        detail = "Cannot add an existing bucket to a generic resource (this is to prevent people using other people their buckets)."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class GrantAccessError(HTTPException):
    def __init__(self, new_user: str):
        detail = f"Can't grant access to '{new_user}', the user needs to be admin or scope_admin)."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class RevokeAccessError(HTTPException):
    def __init__(self, del_user: str, resource_uuid: uuid.UUID):
        detail = f"User '{del_user}' has no access to remove a user from resource/bucket with the UUID '{resource_uuid}'."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class InsufficientPermissionsError(HTTPException):
    def __init__(self):
        detail = "Insufficient permissions to perform the requested operation."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class CannotGrantForGenericResourceException(HTTPException):
    def __init__(self):
        detail = "Cannot grant access to a generic resource."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class CannotRevokeOwnAccessError(HTTPException):
    def __init__(self):
        detail = "Cannot revoke your own access."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ResourceAlreadyExistsError(HTTPException):
    def __init__(self, resource_uuid: uuid.UUID):
        detail = f"A resource with the same credentials, where you have access to, already exists with UUID '{resource_uuid}'."
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class NothingToTransferException(HTTPException):
    def __init__(self):
        detail = "All the files are already in the specified bucket."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
class UserAlreadyHasAccessError(HTTPException):
    def __init__(self, user_id: str, resource_uuid: uuid.UUID):
        detail = f"User with ID '{user_id}' already has access to resource with UUID '{resource_uuid}'."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        
class S3ConnectionException(HTTPException):
    def __init__(self, access_key: str, endpoint: str, region: str | None):
        detail = f"Failed to connect to S3 with access key '{access_key}', endpoint '{endpoint}', and region '{region}'."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class S3FaultyEndpointException(HTTPException):
    def __init__(self, endpoint: str, ending : str, resource_type : ObjectStoreType):
        detail = f"Endpoint '{endpoint}' does not end with {ending} for {resource_type} resource."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class S3NoRegionSpecifiedException(HTTPException):
    def __init__(self, resource_type : ObjectStoreType):
        detail = f"No region specified for {resource_type} resource."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        
class S3PermissionException(HTTPException):
    """Exception raised for errors in the access permissions."""
    def __init__(self, message="Insufficient permissions to perform the requested operation."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)

class S3BucketAlreadyOwnedByYouException(HTTPException):
    """Exception raised when the bucket already exists and is owned by the requester."""
    def __init__(self, bucket_name, message="Bucket already owned by you."):
        detail = f"{message} Bucket Name: {bucket_name}"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class S3BucketAlreadyExistsException(HTTPException):
    """Exception raised when the bucket name is already taken by someone else."""
    def __init__(self, bucket_name, message="Bucket name already exists and is owned by another user."):
        detail = f"{message} Bucket Name: {bucket_name}"
        super().__init__(status_code=status.HTTP_410_GONE, detail=detail)

class S3BucketCreationException(HTTPException):
    """Exception raised for errors during the bucket creation process."""
    def __init__(self, bucket_name, message="An error occurred during the bucket creation process."):
        detail = f"{message} Bucket Name: {bucket_name}"
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class S3BucketCheckFailedException(HTTPException):
    """Exception raised when checking the existence or configuration of an S3 bucket fails."""
    def __init__(self, bucket_name, message="Failed to check S3 bucket."):
        detail = f"{message} Bucket Name: {bucket_name}"
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class S3InvalidBucketNameException(HTTPException):
    """Exception raised when the bucket name does not meet the requirements."""
    def __init__(self, bucket_name, message="Invalid bucket name (must be 3-63 alphanumeric (lowercase) characters, with dashes allowed in the string, no double dashes)."):
        detail = f"{message} Bucket Name: {bucket_name}"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class S3BucketDoesNotExistsException(HTTPException):
    def __init__(self, bucket_name):
        detail = f"Bucket '{bucket_name}' does not exist."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class S3Error(HTTPException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=message)