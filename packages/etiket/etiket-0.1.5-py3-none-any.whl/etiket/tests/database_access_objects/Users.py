import os
os.chdir("../../../")

from etiket.db.data_access_objects.user import dao_user
from etiket.db.get_db_session import SessionLocal

from etiket.db.data_models.user import UserCreate, UserUpdateMe
from etiket.db.types import UserType

import unittest
import time
class test_user_stuff(unittest.TestCase):
    def test_create_and_read_user(self):
        username = "testuser1"
        user_type = UserType.scope_admin
        with SessionLocal() as session:
            user_create = _create_user(username, user_type, session)
            user_db = dao_user.read(username, False, session)
            _delete_user(username, session)
        self.assertEqual(user_create.username, user_db.username)
        self.assertEqual(user_create.firstname, user_db.firstname)
        self.assertEqual(user_create.lastname, user_db.lastname)
        self.assertEqual(user_create.email, user_db.email)
        self.assertEqual(user_type, user_db.user_type)
        self.assertEqual(True, user_db.active)
        self.assertEqual(None, user_db.disable_on)
        
    def test_delete_user(self):
        username = "testuser1"
        user_type = UserType.scope_admin
        with SessionLocal() as session:
            _create_user(username, user_type, session)
            _delete_user(username, session)
            
            users = dao_user.read_all(session)
        
        self.assertEqual(0, len(users))
    
    def test_read_all_users(self):
        with SessionLocal() as session:
            for i in range(20):
                username = f"testuser{i}"
                name = (f"first{i}", f"last{i}")
                _create_user(username, UserType.standard_user, session, name=name)
            for i in range(5):
                username = f"adminuser{i}"
                name = (f"afirst{i}", f"alast{i}")
                _create_user(username, UserType.admin, session, name=name)
            session.commit()

            users = dao_user.read_all(session)
            admin_users = dao_user.read_all(session, user_type=UserType.admin)
            user_query = dao_user.read_all(session, username_query="admin")
        
        self.assertEqual(25, len(users))
        self.assertEqual(5, len(admin_users))
        self.assertEqual(5, len(user_query))
        
        for user in users:
            _delete_user(user.username, session)
    
    def test_update_and_promote_user(self):
        username = "testuser1"
        user_type = UserType.scope_admin
        with SessionLocal() as session:
            _create_user(username, user_type, session)
            
            name = ("Gert", "Eenink")
            userUpdate = UserUpdateMe(firstname=name[0], lastname=name[1], 
                       email=f"{name[0]}.{name[1]}@test.com", 
                        password="23458584")
            dao_user.update(username, userUpdate, session)
            session.commit()
            user_db = dao_user.read(username, False, session)
            self.assertEqual(userUpdate.firstname, user_db.firstname)
            self.assertEqual(userUpdate.lastname, user_db.lastname)
            self.assertEqual(userUpdate.email, user_db.email)

            # test promoting of user :
            dao_user.promote(username, UserType.admin, session)
            session.commit()
            user_db = dao_user.read(username, False, session)
            self.assertEqual(UserType.admin, user_db.user_type)
            _delete_user(username, session)
    
def _create_user(username, user_type ,session, name = ("Mark", "Rutte")):
    create_obj = UserCreate(username=username,firstname=name[0], 
                            lastname=name[1], email=f"{name[0]}.{name[1]}@test.com",
                            password="1234", user_type=user_type)
    dao_user.create(create_obj, session)
    session.commit()
    return create_obj

def _delete_user(username, session):
    dao_user.delete(username, session)
    session.commit()

if __name__ == '__main__':
    from etiket.db.get_db_session import SessionLocal, engine
    from etiket.db.models import *

    Base.metadata.create_all(engine)
    # TODO this test is slow due to password hashing --> fix.
    unittest.main()