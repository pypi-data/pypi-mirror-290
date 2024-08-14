from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_super

from fastapi import APIRouter, Depends, status


from etiket.db.data_access_objects.transfers import dao_S3_transfers
from etiket.db.data_models.transfers import S3FileTransfer
from etiket.db.data_models.token import AccessToken

from typing import List

router = APIRouter(tags=["admin"])

@router.get("/admin/S3/request_transfers/", response_model=List[S3FileTransfer])
def request_transfers(*, approximate_size : int = 10*1024*1024,
                         accessToken: AccessToken = Depends(is_super),
                         session: Session = Depends(get_db_session)):
    return dao_S3_transfers.get_transfers(approximate_size, session)

@router.post("/admin/S3/confirm_transfers/", status_code=status.HTTP_202_ACCEPTED)
def confirm_transfers(*, transfer_updates: List[S3FileTransfer],
                         accessToken: AccessToken = Depends(is_super),
                         session: Session = Depends(get_db_session) ):
    dao_S3_transfers.confirm_transfer(transfer_updates, session)

