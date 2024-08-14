import etiket

from etiket.db.get_db_session import Session, get_db_session
from etiket.web.permissions.permissions import is_any, is_scope_admin, is_admin, is_admin_type, is_super

from fastapi import APIRouter, Depends, Path, Query, status

from etiket.db.data_models.token import AccessToken
from etiket.db.types import SoftwareType
from etiket.db.data_models.versions import VersionRead, VersionCreate, VersionUpdate, ReleaseRead, ReleaseCreate
from etiket.db.data_access_objects.versions import dao_version, dao_release

from typing import List, Optional

router = APIRouter(tags=["version"])

@router.get("/version/API/", response_model=str)
def get_API_version(*, session: Session = Depends(get_db_session) ):
    return etiket.__version__

@router.get("/version/latest/", response_model=VersionRead)
def get_latest_version(*, software_type : SoftwareType, allow_beta : bool = False, session: Session = Depends(get_db_session) ):
    return dao_version.read_latest(software_type, allow_beta, session)

@router.get("/version/", response_model=List[VersionRead])
def get_versions(*, software_type : SoftwareType,
                            min_version : Optional[str] = None, 
                            allow_beta : Optional[bool] = False,
                            session: Session = Depends(get_db_session) ):
    return dao_version.read(min_version, software_type, allow_beta, session)

@router.get("/release/latest/", response_model=ReleaseRead)
def get_latest_release(*, allow_beta: bool = False,
                       session: Session = Depends(get_db_session) ):
    return dao_release.read_latest(allow_beta, session)

@router.get("/release/get_release_from_version/", response_model=ReleaseRead)
def get_release_from_version(*, version : str,
                                software_type : SoftwareType,
                                allow_beta  : bool = False,
                                session: Session = Depends(get_db_session) ):
    return dao_release.read_from_version(version, software_type, allow_beta, session)

@router.post("/release/create/", status_code=status.HTTP_201_CREATED)
def add_release(*, releaseInfo  : ReleaseCreate,
                    accessToken: AccessToken = Depends(is_super),
                    session: Session = Depends(get_db_session)):
    return dao_release.create(releaseInfo, session)

@router.post("/version/create/", status_code=status.HTTP_201_CREATED)
def add_version(*, versionCreate: VersionCreate,
                accessToken: AccessToken = Depends(is_super),
                session: Session = Depends(get_db_session) ):
    return dao_version.create(versionCreate, session)

@router.patch("/version/update/", status_code=status.HTTP_202_ACCEPTED)
def update_version(*, version_id : int,
                    versionUpdate: VersionUpdate,
                    accessToken: AccessToken = Depends(is_super),
                    session: Session = Depends(get_db_session) ):
    return dao_version.update(version_id, versionUpdate, session)