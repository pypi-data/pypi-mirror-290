import datetime

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from etiket.storage.S3_download import S3Download
from etiket.db.types import UserLogStatus
from etiket.db.data_models.user import UserRead
from etiket.settings import settings
class UserLogUploadInfo(BaseModel):
    key : str
    url : str

class UserLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    key : str
    reason : Optional[str] = Field(default=None)
    status : UserLogStatus
    
    user : UserRead
    
    url : Optional[str] = Field(default=None)
    url_expiration_timestamp : Optional[float] = Field(default=None)
    
    created : datetime.datetime

    def model_post_init(self, __context):
        if self.status == UserLogStatus.secured:
            self.url, self.url_expiration_timestamp = S3Download.get_url(settings.S3_LOG_REPORTS_BUCKET_ID, self.key)