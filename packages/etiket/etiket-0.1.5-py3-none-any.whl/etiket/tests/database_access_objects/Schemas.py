import os
os.chdir("../../../")

from etiket.db.data_access_objects.schema import dao_schema
from etiket.db.get_db_session import SessionLocal

from etiket.db.data_models.schema import SchemaCreate, SchemaReadWithScopes, SchemaUpdate

from uuid import uuid4
import unittest

class test_scope_stuff(unittest.TestCase):
    def test_create_and_read_update_delete_scope(self):
        schema_name = "testuser1"
        with SessionLocal() as session:
            schema_create = _create_schema(schema_name, session)
            schema_db = dao_schema.read(schema_create.uuid, session)
            
        self.assertEqual(schema_create.name, schema_db.name)
        self.assertEqual(schema_create.uuid, schema_db.uuid)
        self.assertEqual(schema_create.schema_, schema_db.schema_)
        
        with SessionLocal() as session:
            update = SchemaUpdate(name = "test2", schema={})
            dao_schema.update(schema_create.uuid, update, session)
            session.commit()
            schema_db = dao_schema.read(schema_create.uuid, session)
        
        self.assertEqual(update.name, schema_db.name)
        self.assertEqual(update.schema_, schema_db.schema_)
        
        with SessionLocal() as session:    
            _delete_schema(schema_create.uuid, session)
            schemas = dao_schema.read_all(session)

        self.assertEqual(1, len(schemas))
        
    
def _create_schema(name, session):
    create_obj = SchemaCreate(name = name, uuid=uuid4(), desciption="test", schema={"some_schema": "blah"})
    dao_schema.create(create_obj, session)
    session.commit()
    return create_obj

def _delete_schema(schema_uuid, session):
    dao_schema.delete(schema_uuid, session)
    session.commit()


if __name__ == '__main__':
    from etiket.db.get_db_session import SessionLocal, engine
    from etiket.db.models import *

    Base.metadata.create_all(engine)

    unittest.main()