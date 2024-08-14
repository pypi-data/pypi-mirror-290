from etiket.db.data_models.scope import ScopeReadNoSchema
from etiket.db.data_models.schema_base import SchemaBase, SchemaRead, SchemaData, SchemaAttributes

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

import uuid

class SchemaCreate(SchemaBase):
    pass

class SchemaReadWithScopes(SchemaRead):
    scopes : List[ScopeReadNoSchema]

    
class SchemaUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    name : Optional[str] = Field(default=None)
    description : Optional[str] = Field(default=None)
    schema_ : Optional[SchemaData] = Field(alias='schema', default=None)

class SchemaDelete(BaseModel):
    uuid: uuid.UUID


