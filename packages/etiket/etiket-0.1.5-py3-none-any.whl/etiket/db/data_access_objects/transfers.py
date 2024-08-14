import logging
from sqlalchemy import select, update, func, bindparam, text
from sqlalchemy.orm import Session, selectinload
from typing import List

from etiket.db.data_access_objects.base import dao_base
from etiket.db.data_models.transfers import S3FileTransfer
from etiket.db.get_db_session import database

from etiket.db.models import S3FileTransferOverview, S3ScopeTransferOverview, Files

from etiket.db.types import S3FileTransferStatus, S3ScopeTransferStatus

logger = logging.getLogger(__name__)

class dao_S3_transfers(dao_base):
    @staticmethod
    def get_transfers(approximate_size, session: Session) -> List[S3FileTransfer]:        
        '''
        Get a list of transfers that are pending and that are below the approximate size.
        
        :param approximate_size: The approximate size of the files to transfer (default 10MB). Will at least fetch one file if the size is above the approximate size.
        :param session: The database session.
        
        :return: A list of S3FileTransfer objects.
        '''
        
        try:
            # TODO allow also to fetch failed items
            
            with database.get_session_factory().begin() as sess:
                # lock table to prevent that two requests start doing the subquery at the same time.
                sess.execute(text(f"LOCK TABLE {S3FileTransferOverview.__tablename__} IN EXCLUSIVE MODE"))
                
                cte = select(S3FileTransferOverview.id, func.sum(Files.size).over(order_by=S3FileTransferOverview.id).label('total_size'))
                cte = cte.join(S3FileTransferOverview.file)
                cte = cte.where(S3FileTransferOverview.status == S3FileTransferStatus.PENDING).cte()
                
                sub_query = select(cte.c.id).where(cte.c.total_size <= approximate_size)
                sub_query = sub_query.union(select(cte.c.id).where(cte.c.total_size > approximate_size).limit(1))
                
                stmt = update(S3FileTransferOverview).where(S3FileTransferOverview.id.in_(sub_query)).values(status=S3FileTransferStatus.IN_PROGRESS)
                stmt = stmt.returning(S3FileTransferOverview.id)
                
                update_ids = sess.execute(stmt).scalars().all()
            
            stmt = select(S3FileTransferOverview).where(S3FileTransferOverview.id.in_(update_ids))
            stmt = stmt.options(selectinload(S3FileTransferOverview.file), selectinload(S3FileTransferOverview.transfer))
        
            results = session.execute(stmt).scalars().all()
            
            transfers = []
            
            for res in results:
                res.transfer.status = S3ScopeTransferStatus.IN_PROGRESS
                transfer = S3FileTransfer(  transfer_id=res.id,
                                            file_id=res.file_id, scope_transfer_id=res.transfer.id,
                                            file_size=res.file.size, bucket_src_id=res.file.bucket_id,
                                            bucket_dst_id=res.transfer.bucket_id, s3_key=res.file.s3_key,
                                            status=S3FileTransferStatus.PENDING)
                transfers.append(transfer)
            
            session.commit()
            
            return transfers
        
        except Exception as e:
            session.rollback()
            logger.exception(e)
            raise e
        
    @staticmethod
    def confirm_transfer(transferList : List[S3FileTransfer], session: Session):
        # set transfer id to set the status to completed or failed.
        bytes_transferred = {}
        update_file_transfer_status = []
        update_file_bucket = []
        for transfer in transferList:
            update_file_transfer_status.append({"id": transfer.transfer_id, "status": transfer.status})
            if transfer.status == S3FileTransferStatus.COMPLETED:
                bytes_transferred[transfer.scope_transfer_id] = bytes_transferred.get(transfer.scope_transfer_id, 0) + transfer.file_size
                update_file_bucket.append({"id": transfer.file_id, "bucket_id": transfer.bucket_dst_id})
                
        session.execute(update(S3FileTransferOverview), update_file_transfer_status)
        session.execute(update(Files), update_file_bucket)
        
        # add bytes transferred and update status if needed.
        for scope_transfer_id, bytes in bytes_transferred.items():
            stmt = select(S3ScopeTransferOverview).where(S3ScopeTransferOverview.id == scope_transfer_id)
            transfer = session.execute(stmt).scalar()
            transfer.bytes_transferred += bytes
            
            stmt = select(func.COUNT(S3FileTransferOverview.id)).where(S3FileTransferOverview.transfer_id == scope_transfer_id)
            stmt = stmt.where(S3FileTransferOverview.status.in_([S3FileTransferStatus.PENDING, S3FileTransferStatus.IN_PROGRESS]))
            
            if session.execute(stmt).scalar() == 0:
                stmt = select(func.COUNT(S3FileTransferOverview.id)).where(S3FileTransferOverview.transfer_id == scope_transfer_id)
                stmt = stmt.where(S3FileTransferOverview.status == S3FileTransferStatus.FAILED)
                
                n_failed = session.execute(stmt).scalar()
                if n_failed == 0:
                    transfer.status = S3ScopeTransferStatus.COMPLETED
                else:
                    transfer.status = S3ScopeTransferStatus.FAILED
                    transfer.error_message = f"{n_failed} files failed to transfer, please try again or contact support."
        
        session.commit()