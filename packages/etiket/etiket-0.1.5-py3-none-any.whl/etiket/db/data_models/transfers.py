from pydantic import BaseModel

from etiket.db.types import S3FileTransferStatus

class S3FileTransfer(BaseModel):
    transfer_id : int
    scope_transfer_id : int
    file_id : int
    file_size : int
    bucket_src_id : int
    bucket_dst_id : int
    s3_key : str
    status : S3FileTransferStatus
    delete_on_completion : bool = False