from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_super

from fastapi import APIRouter, Depends, status

from etiket.storage.S3_upload import S3Upload
from etiket.storage.S3_keygen import generate_key_4_logging

from etiket.db.data_models.user_logs import UserLogRead, UserLogUploadInfo
from etiket.db.data_access_objects.user_logs import dao_user_logs
from etiket.db.data_models.token import AccessToken

from etiket.settings import settings

from typing import List, Optional

router = APIRouter(tags=["logs"])

@router.post("/logs/deposit/create/", response_model=UserLogUploadInfo)
def deposit_log_create(*,
                       file_name : str,
                       reason: Optional[str] = None,
                       accessToken: AccessToken = Depends(is_any),
                       session: Session = Depends(get_db_session) ) :
    key = generate_key_4_logging(accessToken.sub, file_name)
    dao_user_logs.create(accessToken.sub, key, reason, session)
    
    url = S3Upload.create_single(settings.S3_LOG_REPORTS_BUCKET_ID, key, 0)
    
    return UserLogUploadInfo(key = key, url = url)

@router.post("/logs/deposit/confirm/", status_code=status.HTTP_202_ACCEPTED)
def deposit_log_confirm(*,
                        key: str,
                        accessToken: AccessToken = Depends(is_any),
                        session: Session = Depends(get_db_session) ):
    S3Upload.check_upload_single_part(settings.S3_LOG_REPORTS_BUCKET_ID, key)
    dao_user_logs.confirm(key, accessToken.sub, session)

@router.get("/logs/", response_model=List[UserLogRead])
def get_logs(*, username : Optional[str] = None,
                offset : Optional[int] = 0,
                limit : Optional[int] = 100,
                accessToken: AccessToken = Depends(is_super),
                session: Session = Depends(get_db_session)):
    return dao_user_logs.read_many(username, offset, limit, session)

@router.get("/logs/me/", response_model=List[UserLogRead])
def get_my_logs(*,
                offset : Optional[int] = 0,
                limit : Optional[int] = 100,
                accessToken: AccessToken = Depends(is_any),
                session: Session = Depends(get_db_session)):
    return dao_user_logs.read(accessToken.sub, offset, limit, session)