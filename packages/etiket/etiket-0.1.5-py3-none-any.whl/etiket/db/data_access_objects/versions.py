from typing import Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import update, select, func, exc

from fastapi import HTTPException

from etiket.db.models import software_releases, software_versions
from etiket.db.data_models.versions import VersionRead, VersionCreate, VersionUpdate, ReleaseRead, ReleaseCreate
from etiket.db.types import SoftwareType

from packaging.version import Version


class dao_version:   
    @staticmethod
    def create(versionCreate: VersionCreate, session: Session) -> None:
        last_version = None
        try:
            last_version = dao_version.read_latest(versionCreate.type, versionCreate.needs_update, session)
        except HTTPException: # if no version is found
            pass
        
        if last_version is not None:
            if Version(versionCreate.version) <= Version(last_version.version):
                raise HTTPException(status_code=400, detail=f"The version number should be greater than the last version number {last_version.version}")
        
        
        new_version = software_versions(**versionCreate.model_dump())
        session.add(new_version)
        session.commit()

    @staticmethod
    def update(version_id: int, versionUpdate: VersionUpdate, session: Session) -> None:
        stmt = select(software_versions).where(software_versions.id == version_id)
        if session.execute(stmt).scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Version not found")
        
        try :
            stmt = (update(software_versions).
                    where(software_versions.id == version_id).
                    values(versionUpdate.model_dump(exclude_unset=True))
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        
    @staticmethod
    def read(min_version: Optional[str], software_type: SoftwareType, allow_beta : bool, session: Session = None) -> List[VersionRead]:
        formatted_version = min_version.split('-')[0] if min_version is not None else None
        versions = dao_version.__read(formatted_version, software_type, allow_beta, None, session)
        
        if allow_beta is False or min_version is None:
            return versions
        # this is needed if the input is a beta version (cannot be checked in the database (or at least not with the current script))
        return [version for version in versions if Version(version.version.replace('-', '.')) >= Version(min_version.replace('-', '.'))]

    @staticmethod
    def read_latest(software_type: SoftwareType, allow_beta: bool, session: Session) -> VersionRead:
        latest = dao_version.__read(None, software_type, allow_beta, 1, session)
        if len(latest) == 0:
            raise HTTPException(status_code=404, detail=f"No {software_type} version found.")
        
        return latest[0]
    
    @staticmethod
    def __read(min_version: Optional[str], software_type: SoftwareType, allow_beta : bool, limit : Optional[int], session: Session = None) -> List[VersionRead]:
        stmt = select(software_versions).where(software_versions.type == software_type)
        if min_version:
            stmt = stmt.where(func.compare_sem_version(software_versions.version, min_version))
        if allow_beta is False:
            stmt = stmt.where(software_versions.version.not_like('%-%'))
        if limit:
            stmt = stmt.limit(limit)
        stmt = stmt.order_by(software_versions.id.desc())

        results = session.execute(stmt).scalars().all()
        return [VersionRead.model_validate(result) for result in results]
    
    @staticmethod 
    def read_by_id(version_id: int, session: Session) -> VersionRead:
        stmt = select(software_versions).where(software_versions.id == version_id)
        version = session.execute(stmt).scalar_one_or_none()
        if version is None:
            raise HTTPException(status_code=404, detail="Version not found")
        
        return VersionRead.model_validate(version)
    
    @staticmethod
    def read_by_version_and_type(version: str, software_type: SoftwareType, session: Session) -> VersionRead:
        stmt = select(software_versions).where(software_versions.version == version, software_versions.type == software_type)
        version = session.execute(stmt).scalar_one_or_none()
        if version is None:
            raise HTTPException(status_code=404, detail="Version not found")
        
        return VersionRead.model_validate(version)
    
class dao_release:
    @staticmethod
    def create(releaseCreate: ReleaseCreate, session: Session):
        last_etiket = dao_version.read_latest(SoftwareType.etiket, releaseCreate.beta_release, session)
        last_dataQruiser = dao_version.read_latest(SoftwareType.dataQruiser, releaseCreate.beta_release, session)
        last_qdrive = dao_version.read_latest(SoftwareType.qdrive, releaseCreate.beta_release, session)
        
        try :
            last_release = dao_release.read_latest(releaseCreate.beta_release, session)
        except HTTPException:
            last_release = None
        
        if ( last_release is not None and
             last_release.etiket_version.id == last_etiket.id and 
             last_release.dataQruiser_version.id == last_dataQruiser.id and 
             last_release.qdrive_version.id == last_qdrive.id ) :
            raise HTTPException(status_code=400, detail=f"Cannot create a release with the same versions as the last release (release id: {last_release.release_id})")
        
        # validate minimal versions  
        min_etiket = dao_version.read_by_id(releaseCreate.min_version_etiket_id, session)
        if (min_etiket.type != SoftwareType.etiket):
            raise HTTPException(status_code=400, detail="The minimal version for etiket should be of type etiket")
        if releaseCreate.beta_release is False and min_etiket.version.find('-') != -1:
            raise HTTPException(status_code=400, detail="The minimal version for etiket should not be a beta version")
        
        min_dataQruiser = dao_version.read_by_id(releaseCreate.min_version_dataQruiser_id, session)
        if (min_dataQruiser.type != SoftwareType.dataQruiser):
            raise HTTPException(status_code=400, detail="The minimal version for dataQruiser should be of type dataQruiser")
        if releaseCreate.beta_release is False and min_dataQruiser.version.find('-') != -1:
            raise HTTPException(status_code=400, detail="The minimal version for dataQruiser should not be a beta version")
        
        min_qdrive = dao_version.read_by_id(releaseCreate.min_version_qdrive_id, session)
        if (min_qdrive.type != SoftwareType.qdrive):
            raise HTTPException(status_code=400, detail="The minimal version for qdrive should be of type qdrive")
        if releaseCreate.beta_release is False and min_qdrive.version.find('-') != -1:
            raise HTTPException(status_code=400, detail="The minimal version for qdrive should not be a beta version")
        
        new_release = software_releases(beta_release = releaseCreate.beta_release,
                                        etiket_version_id = last_etiket.id,
                                        dataQruiser_version_id = last_dataQruiser.id,
                                        qdrive_version_id = last_qdrive.id,
                                        min_etiket_version_id = releaseCreate.min_version_etiket_id,
                                        min_dataQruiser_version_id = releaseCreate.min_version_dataQruiser_id,
                                        min_qdrive_version_id = releaseCreate.min_version_qdrive_id)
        
        session.add(new_release)
        session.commit()

        
    @staticmethod
    def read_latest(allow_beta: bool, session: Session):
        stmt = select(software_releases).order_by(software_releases.id.desc())
        if not allow_beta:
            stmt = stmt.where(software_releases.beta_release == False)
        stmt = stmt.limit(1)
        
        try :
            return ReleaseRead.model_validate(session.execute(stmt).scalar_one())
        except exc.NoResultFound:
            raise HTTPException(status_code=404, detail="No release made yet.")
        
    @staticmethod
    def read_from_version(version : str, software_type : SoftwareType, allow_beta: bool, session: Session):
        stmt = select(software_releases)
        versionInfo = dao_version.read_by_version_and_type(version, software_type, session)
        if versionInfo.type == SoftwareType.etiket:
            stmt = stmt.where(software_releases.etiket_version_id == versionInfo.id)
        elif versionInfo.type == SoftwareType.dataQruiser:
            stmt = stmt.where(software_releases.dataQruiser_version_id == versionInfo.id)
        elif versionInfo.type == SoftwareType.qdrive:
            stmt = stmt.where(software_releases.qdrive_version_id == versionInfo.id)
        else:
            raise HTTPException(status_code=404, detail="Version of the type %s is not supported" % versionInfo.type)

        if not allow_beta:
            stmt = stmt.where(software_releases.beta_release == False)
        
        stmt = stmt.order_by(software_releases.id.desc()).limit(1)
        
        try :
            return ReleaseRead.model_validate(session.execute(stmt).scalar_one())
        except exc.NoResultFound:
            raise HTTPException(status_code=404, detail="No release found for the given software version.")