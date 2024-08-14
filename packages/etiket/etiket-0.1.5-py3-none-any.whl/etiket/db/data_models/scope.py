from etiket.db.data_models.schema_base import SchemaRead
from etiket.db.data_models.user_base import UserRead
from etiket.db.types import scopestr

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

import datetime, uuid


class ScopeBase(BaseModel):
    name : scopestr
    uuid : uuid.UUID
    description: str

class ScopeCreate(ScopeBase):
    bucket_uuid : uuid.UUID

class ScopeReadNoSchema(ScopeBase):
    model_config = ConfigDict(from_attributes=True)

    archived: bool

class ScopeRead(ScopeReadNoSchema):    
    created: datetime.datetime
    modified: datetime.datetime
    
    schema_: Optional["SchemaRead"] = Field(alias="schema")

class ScopeReadWithUsers(ScopeRead):
    users : List["UserRead"]

class ScopeUpdate(BaseModel):
    name : Optional[scopestr] = Field(default = None)
    description: Optional[str] = Field(default = None)
    archived: Optional[bool] = Field(default = None)

class ScopeDelete(BaseModel):
    uuid : uuid.UUID
    