from etiket.exceptions.exceptions import DatasetCreateUIDUUIDException

from etiket.db.data_models.file import FileRead
from etiket.db.data_models.scope import ScopeRead

from etiket.db.types import datasetstr

from pydantic import BaseModel, Field, model_validator, \
    field_validator, ConfigDict
from typing import Optional, List

import datetime, uuid

class DatasetBase(BaseModel):
    uuid : uuid.UUID
    alt_uid : Optional[str] = Field(default=None)
    collected : datetime.datetime
    name: str
    creator : str
    description : Optional[str] = Field(default=None)
    notes : Optional[str] = Field(default=None)
    keywords : List[str]
    ranking : int

class DatasetCreate(DatasetBase):
    scope_uuid : uuid.UUID
    attributes : Optional[dict[str, str]] = Field(default_factory=dict)
    
    @model_validator(mode='after')
    def same_identifier_check(self):
        if self.alt_uid != str(self.uuid):
            return self
        raise DatasetCreateUIDUUIDException(self.uuid, self.alt_uid)

class DatasetRead(DatasetBase):
    model_config = ConfigDict(from_attributes=True)

    created : datetime.datetime
    modified : datetime.datetime

    scope : ScopeRead
    attributes : Optional[dict[str, str]] = Field(default={})
    files : List["FileRead"]
    
    @field_validator('attributes', mode='before')
    @classmethod
    def convert_orm_type_to_dict(cls, attributes):
        out = {}
        for attr in attributes:
            out[attr.key]= attr.value
        return out
        
class DatasetUpdate(BaseModel):
    alt_uid : Optional[str] = Field(default=None)
    name:  Optional[datasetstr] = Field(default=None)
    description : Optional[str] = Field(default=None)
    notes : Optional[str] = Field(default=None)
    keywords :  Optional[List[str]] = Field(default=None)
    ranking :  Optional[int] = Field(default=None)
    
    attributes : Optional[dict[str, str]] = Field(default={})

class DatasetDelete(BaseModel):
    uuid : uuid.UUID
    
class DatasetSelection(BaseModel):
    scope_uuids : Optional[List[uuid.UUID]] = Field(default=None)
    attributes : Optional[dict[str, List[str]]] = Field(default={})
    
class DatasetSearch(DatasetSelection):
    search_query : Optional[str] = Field(default=None)
    ranking : Optional[int] = Field(default=0)
    has_notes : Optional[bool] = Field(default=False)
    
    start_date : Optional[datetime.datetime] = Field(default=None)
    end_date : Optional[datetime.datetime] = Field(default=None)
    time_zone : Optional[str] = Field(default=None)