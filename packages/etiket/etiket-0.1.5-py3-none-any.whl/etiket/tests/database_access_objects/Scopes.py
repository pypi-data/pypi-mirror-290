import os
os.chdir("../../../")

from etiket.db.get_db_session import SessionLocal
from etiket.db.types import UserType

from etiket.db.data_access_objects.user import dao_user
from etiket.db.data_access_objects.scope import dao_scope
from etiket.db.data_access_objects.schema import dao_schema

from etiket.db.data_models.user import UserCreate, UserRead, ScopeRead
from etiket.db.data_models.scope import ScopeUpdate, ScopeCreate, ScopeRead
from etiket.db.data_models.schema import SchemaCreate, SchemaReadWithScopes, SchemaUpdate

from uuid import uuid4, UUID
import unittest

class test_scope_stuff(unittest.TestCase):
    def test_create_and_read_update_delete_scope(self):
        scope_name = "testuser1"
        with SessionLocal() as session:
            scope_create = _create_scope(scope_name, session)
            scope_db = dao_scope.read(scope_create.uuid, session)
            
        self.assertEqual(scope_create.name, scope_db.name)
        self.assertEqual(scope_create.uuid, scope_db.uuid)
        self.assertEqual(scope_create.description, scope_db.description)
        self.assertEqual(False, scope_db.archived)
        
        with SessionLocal() as session:
            update = ScopeUpdate(name = "test2", description="description changed", archived=True)
            dao_scope.update(scope_create.uuid, update, session)
            session.commit()
            scope_db = dao_scope.read(scope_create.uuid, session)
            
        self.assertEqual(update.name, scope_db.name)
        self.assertEqual(update.description, scope_db.description)
        self.assertEqual(update.archived, scope_db.archived)
        
        with SessionLocal() as session:    
            _delete_scope(scope_create.uuid, session)
            scopes = dao_scope.read_all(session=session)
        
        # self.assertEqual(0, len(scopes))
        
    def test_add_read_and_remove_users_from_scope(self):
        # create some users, add them to the scope 
        # the check if they are in the scope, then remove.
        # check again
        scope_name = "test"
        with SessionLocal() as session:
            scope_create = _create_scope(scope_name, session)
            users = _create_users(5, session)

            for user in users:
                dao_scope.assign_user(scope_create.uuid, user.username, session)
            session.commit()
            scope_read = dao_scope.read(scope_create.uuid, session=session)
            
            self.assertCountEqual(users, scope_read.users)
            
            _delete_users(users, session)
            _delete_scope(scope_create.uuid, session)

    def test_assignement_of_schemas(self):
        scope_name = "test"
        with SessionLocal() as session:
            scope_create = _create_scope(scope_name, session)
            schema_1 = _create_schema("schema_1", session)
            schema_2 = _create_schema("schema_1", session)
            
            dao_scope.assign_schema(scope_create.uuid, schema_1.uuid, session)
            session.commit()
            scope = dao_scope.read(scope_create.uuid, session)
            self.assertEqual(scope.schema_.uuid, schema_1.uuid)
            dao_scope.assign_schema(scope_create.uuid, schema_2.uuid, session)
            session.commit()
            scope = dao_scope.read(scope_create.uuid, session)
            self.assertEqual(scope.schema_.uuid, schema_2.uuid)
            dao_scope.remove_schema(scope_create.uuid, session)
            scope = dao_scope.read(scope_create.uuid, session)
            self.assertEqual(scope.schema_, None)
            
            _delete_schema(schema_1.uuid, session)
            _delete_schema(schema_2.uuid, session)
            _delete_scope(scope_create.uuid, session)
            
def _create_scope(name, session):
    create_obj = ScopeCreate(name = name, uuid=uuid4(), description="test-scope")
    dao_scope.create(create_obj, session)
    session.commit()
    return create_obj

def _delete_scope(scope_uuid, session):
    dao_scope.delete(scope_uuid, session)
    session.commit()

def _create_users(n_users, session):
    users = []
    for i in range(n_users):
        username = f"testuser{i}"
        name = (f"first{i}", f"last{i}")
        create_obj = UserCreate(username=username,firstname=name[0], 
                                lastname=name[1], email=f"{name[0]}.{name[1]}@test.com",
                                password="1234", user_type=UserType.standard_user)
        try:
            user  = dao_user.create(create_obj, session)
        except:
            user = dao_user.read(create_obj.username, False, session)
        session.commit()
        users.append(UserRead.model_validate(user))
    return users

def _delete_users(users, session):
    for user in users: 
        dao_user.delete(user.username, session)
    session.commit()


def _create_schema(name, session):
    create_obj = SchemaCreate(name = name, uuid=uuid4(), schema={"some_schema": "blah"})
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