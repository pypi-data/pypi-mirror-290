from typing import Optional

from etiket.exceptions.exceptions import FailedToCreateDownloadLink
from etiket.settings import settings

from etiket.storage.client import S3BucketMgr

from datetime import datetime

import logging

logger = logging.getLogger(__name__)
class S3Download:
    @staticmethod
    def get_url(bucket_id : int, key : str, file_name : Optional[str] = None):
        try:
            # TODO investigate the usefullness/need for multipart downloads
            # TODO this should only take 0.2 ms but it seems to take an average of 1ms per file
            bucket_info = S3BucketMgr.get_bucket(bucket_id)
            
            params = {'Bucket': bucket_info.name,'Key': key}
            if file_name: # filename is inferred from key if not provided
                params['ResponseContentDisposition'] = f'attachment; filename="{file_name}"'
            
            url = bucket_info.client.generate_presigned_url(
                ClientMethod='get_object',
                Params=params,
                ExpiresIn = settings.S3_PRESIGN_EXPIRATION_DOWNLOAD
            )
        except Exception:
            logger.exception("Failed to create download link for key %s with bucket id %s", key, bucket_id)
            raise FailedToCreateDownloadLink(key)

        exp = datetime.now().timestamp() + settings.S3_PRESIGN_EXPIRATION_DOWNLOAD
        return url, exp