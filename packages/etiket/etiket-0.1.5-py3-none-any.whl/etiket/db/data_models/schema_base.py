from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List

import datetime, uuid, re

from etiket.exceptions.exceptions import SchemaNotValidException

class SchemaData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    attributes : List['SchemaAttributes']

class SchemaAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    is_required : bool
    default_values : List[str] = Field(default_factory=lambda:[])
    regex_validation : Optional[str] = Field(default=None)

    @field_validator('regex_validation')
    @classmethod
    def is_valid_regex(cls, v: str) -> str:
        if v is not None:
            try:
                re.compile(v)
            except re.error:
                raise SchemaNotValidException(f'the regex "{v}" is invalid.')
        return v

class SchemaBase(BaseModel):
    uuid : uuid.UUID
    name : str
    description: str = Field(default='')
    schema_ : 'SchemaData' = Field(alias='schema')

class SchemaRead(SchemaBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    created: datetime.datetime
    modified: datetime.datetime