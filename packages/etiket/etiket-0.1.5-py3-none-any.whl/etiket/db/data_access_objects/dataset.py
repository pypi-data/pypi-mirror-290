from sqlalchemy.orm import Session, selectinload, joinedload, aliased
from sqlalchemy import select, func, delete, Date, text, desc, Select, and_

from typing import List, Optional
from uuid import UUID

from etiket.exceptions.exceptions import DatasetAlreadyExistException,\
    DatasetAltUIDAlreadyExistException, DatasetNotFoundException, DatasetNotFoundExceptionUID
from etiket.db.models import Scopes, Datasets, DatasetAttr, DsAttrLink

from etiket.db.data_access_objects.base import dao_base
from etiket.db.data_access_objects.scope import _get_scope_raw

from etiket.db.data_models.dataset import  DatasetCreate, DatasetRead,\
    DatasetUpdate, DatasetSearch, DatasetSelection

class dao_dataset(dao_base):
    @staticmethod
    def create(datasetCreate : DatasetCreate, session : Session):
        scope = _get_scope_raw(datasetCreate.scope_uuid, session)
        
        if not dao_dataset._unique(Datasets, Datasets.uuid == datasetCreate.uuid, session):
            raise DatasetAlreadyExistException(datasetCreate.uuid)
        if (datasetCreate.alt_uid is not None and 
            not dao_dataset._unique(Datasets, (Datasets.alt_uid == datasetCreate.alt_uid) & (Datasets.scope_id == scope.id), session)):
                raise DatasetAltUIDAlreadyExistException(datasetCreate.alt_uid)
        
        ds = Datasets(**datasetCreate.model_dump( by_alias=True, exclude=["scope_uuid", "attributes"]),
                      search_helper=_gen_search_helper(datasetCreate))
        
        ds.scope = scope
        
        for k,v in datasetCreate.attributes.items():
            attr = _get_or_create_attr(k,v, scope, session)
            ds.attributes.append(attr)

        session.add(ds)
        session.commit()
        return ds
    
    @staticmethod
    def read(ds_uuid : UUID, scope_ids : Optional[List[UUID]], session : Session):
        dataset_db = _get_ds_by_uuid(ds_uuid, scope_ids, session)
        return DatasetRead.model_validate(dataset_db)
    
    @staticmethod
    def read_by_alt_uid(alt_uid : str, scope_id : int, session : Session):
        stmt = select(Datasets).where(Datasets.alt_uid == alt_uid).where(Datasets.scope_id == scope_id)
        result = session.execute(stmt).scalar_one_or_none()
        if not result:
            raise DatasetNotFoundExceptionUID(alt_uid)
        return DatasetRead.model_validate(result)
    
    @staticmethod
    def update(ds_uuid : UUID, datasetUpdate : DatasetUpdate, session : Session):
        dataset_db = _get_ds_by_uuid(ds_uuid, None ,session)
        dao_dataset._update(dataset_db, datasetUpdate, session,
                             exclude=["attributes"])
        
        dataset_db.search_helper = _gen_search_helper(dataset_db)

        # sqlalchemy does not seem to have many tools to do this automatically, so going manual ..
        if datasetUpdate.attributes:
            attr_to_delete = []
            for attribute in dataset_db.attributes : 
                if attribute.key in datasetUpdate.attributes.keys():
                    if attribute.value == datasetUpdate.attributes[attribute.key]:
                        datasetUpdate.attributes.pop(attribute.key)
                        continue
                attr_to_delete.append(attribute.id)
                dataset_db.attributes.remove(attribute)
            session.commit()

            dao_dataset.__assign_attributs(dataset_db, datasetUpdate.attributes, session)
            dao_dataset.__remove_unlinked_attributes(attr_to_delete, session)       
        
    @staticmethod
    def delete(ds_uuid : UUID, session : Session):
        ds = _get_ds_by_uuid(ds_uuid, None, session)
        attr_id = [attr.id for attr in ds.attributes]
        session.delete(ds)
        session.commit()
        dao_dataset.__remove_unlinked_attributes(attr_id, session)
    
    @staticmethod
    def search(datasetSearch: DatasetSearch, scope_ids : List[int], session : Session, offset: str = None, limit : str = None):
        stmt = select(Datasets)
        stmt = stmt.options(selectinload(Datasets.files), selectinload(Datasets.attributes) )

        stmt = dao_dataset.__search_query(stmt, datasetSearch, scope_ids)
        stmt = stmt.order_by(desc(Datasets.collected))
        stmt = stmt.offset(offset).limit(limit)

        result = session.execute(stmt).scalars()
        return [DatasetRead.model_validate(res) for res in result]
    
    @staticmethod
    def search_for_uuid_or_uid(uuid_or_uid : str, scope_ids : List[int], session : Session):
        condition = (Datasets.alt_uid == uuid_or_uid)
        is_uuid = False
        try:
            uuid = UUID(uuid_or_uid)
            condition = condition | (Datasets.uuid == uuid)
            is_uuid = True
        except ValueError:
            pass
        
        stmt = select(Datasets).where(Datasets.scope_id.in_(scope_ids))
        stmt = stmt.where(condition)
        stmt = stmt.order_by(desc(Datasets.collected))
        result = session.execute(stmt).scalars().all()
        return [DatasetRead.model_validate(res) for res in result], is_uuid
    
    @staticmethod
    def get_distinct_dates(datasetSearch : DatasetSearch, scope_ids : List[int], session : Session, offset : int = None, limit : int = None):        
        stmt = select(func.DATE(Datasets.collected))
        stmt = dao_dataset.__search_query(stmt, datasetSearch, scope_ids)
        stmt = stmt.order_by(Datasets.collected.cast(Date).desc()).offset(offset).limit(limit)

        return session.execute(stmt.distinct()).scalars().all()

    @staticmethod
    def get_attributes(datasetSelection : DatasetSelection, scope_ids : List[int], session: Session):
        # TODO test if performance of this query is sufficient
        valid_ids = dao_dataset.__select_ds_id_from_attr_query(scope_ids, datasetSelection.attributes)
        stmt = select(DatasetAttr.key, DatasetAttr.value).join(DsAttrLink).where(DsAttrLink.dataset_id.in_(valid_ids)).group_by(DatasetAttr.id)
        result = session.execute(stmt).all()

        keys = set([res[0] for res in result])
        out = {key : [] for key in keys}
        
        for res in result:
            out[res[0]].append(res[1])
        
        return out

    @staticmethod
    def get_scope_uuid_from_ds_uuid(dataset_uuid : UUID, session: Session):
        ds = _get_ds_by_uuid(dataset_uuid, None, session)
        return ds.scope.uuid
        
    @staticmethod
    def __assign_attributs(model, attributes, session):
        for k,v in attributes.items():
            attr = _get_or_create_attr(k,v, model.scope, session)
            model.attributes.append(attr)
            
    @staticmethod
    def __remove_unlinked_attributes(attr_id_list : List[int], session : Session):
        to_delete =[]
        for i in attr_id_list: # TODO find a cleaner way to do this as in a loop (on the other hand not many attr expected).
            stmt = select(func.count("*")).where(DsAttrLink.dataset_attr_id == i)
            if session.execute(stmt).scalar_one() == 0:
                to_delete.append(i)
        session.execute(delete(DatasetAttr).where(DatasetAttr.id.in_(to_delete)))
        session.commit()

    @staticmethod
    def __select_ds_id_from_attr_query(scope_ids: List[int], attr: dict[str, List[str]]):
        stmt = select(DsAttrLink.dataset_id).join(DatasetAttr).where(DatasetAttr.scope_id.in_(scope_ids))
        if attr:
            where_query = None
            for k,v in attr.items():
                cond = ((DatasetAttr.key == k) & DatasetAttr.value.in_(v))
                if where_query is not None:
                    where_query = where_query | (DatasetAttr.scope_id.in_(scope_ids)) & cond
                else:
                    where_query = cond
            stmt = stmt.where(where_query)

            if len(attr) > 1:
                stmt = stmt.having(func.count('*') >= len(attr))
        
        stmt = stmt.group_by(DsAttrLink.dataset_id)

        return stmt

    @staticmethod
    def __search_query(stmt : Select, datasetSearch: DatasetSearch, scope_ids: List[int]):
        if datasetSearch.search_query:
            datasetSearch.search_query = datasetSearch.search_query.replace(":", " ").replace("(", " ").replace(")", " ").replace("!", " ").replace("&", " ").replace("|", " ").replace("*", " ")
            search_query = " ".join([word + ":*" for word in datasetSearch.search_query.split()])# add :* after every word to match every beginning of the word
            search_query = " & ".join(search_query.split()) #add & in between words
            stmt = stmt.where(
                func.to_tsvector(text("'simple'"), Datasets.search_helper)
                .op('@@')(func.to_tsquery(text("'simple'"), text(":search_term")))
            ).params(search_term= search_query) 

        stmt = stmt.where(Datasets.scope_id.in_(scope_ids))
        
        if datasetSearch.start_date:
            stmt = stmt.where(Datasets.collected >= datasetSearch.start_date)
        if datasetSearch.end_date:
            stmt = stmt.where(Datasets.collected <= datasetSearch.end_date)
        if datasetSearch.has_notes:
            stmt = stmt.where(Datasets.notes.is_not(None))
        if datasetSearch.ranking:
            stmt = stmt.where(Datasets.ranking >= datasetSearch.ranking)
        
        if datasetSearch.attributes:
            valid_ids = dao_dataset.__select_ds_id_from_attr_query(scope_ids, datasetSearch.attributes)
            stmt = stmt.where(Datasets.id.in_(valid_ids))
        
        return stmt

# TODO convert this in an autogenerated TS_VECTOR column
def _gen_search_helper(model : Datasets):
    search_helper = f"{model.name}"
    if model.description: search_helper += f" {model.description}"
    if model.notes: search_helper += f" {model.notes}"

    for kw in model.keywords:
        search_helper += f" {kw}"
    return search_helper

def _get_ds_by_uuid(uuid : UUID, scope_ids : Optional[List[int]], session : Session):   
    stmt = select(Datasets).where(Datasets.uuid == uuid)
    if scope_ids is not None:
        stmt = stmt.where(Datasets.scope_id.in_(scope_ids))
    stmt.options(selectinload(Datasets.files), selectinload(Datasets.attributes))
    
    result = session.execute(stmt).scalar_one_or_none()
    if not result:
        raise DatasetNotFoundException(uuid)
    
    return result

def _get_or_create_attr(key, value, scope : Scopes, session:Session):
    stmt = select(DatasetAttr).where(DatasetAttr.scope_id == scope.id)
    stmt = stmt.where(DatasetAttr.key == key)
    stmt = stmt.where(DatasetAttr.value == value)
    
    result = session.execute(stmt).scalar_one_or_none()
    
    if result is None:
        return DatasetAttr(key=key, value=value, scope_id = scope.id)
    
    return result