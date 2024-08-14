from fastapi.testclient import TestClient
from etiket.tests.set_up_testing_environment import *

from etiket.main import app
from etiket.settings import settings

from etiket.db.data_models.user import UserCreate
from etiket.db.data_models.scope import ScopeCreate
from etiket.db.data_models.dataset import DatasetCreate, DatasetSearch

from etiket.db.types import UserType

from fastapi.encoders import jsonable_encoder
import unittest, json, uuid, datetime

class test_user_endpoint(unittest.TestCase):
    def test_user_creation(self):
        with TestClient(app) as client:
            super_user_token = _login_user(client, settings.ETIKET_ADMIN_USERNAME, settings.ETIKET_ADMIN_PASSWORD)
            scope_uuids = _create_test_scenario(client, super_user_token)
            scope1 = scope_uuids[0]
            scope2 = scope_uuids[1]
            
            standard2_token = _login_user(client, "standard2", "standard2")
            standard2_headers = {"Authorization": f"Bearer {standard2_token}"}
            
            admin_token = _login_user(client, "admin", "admin")
            admin_headers = {"Authorization": f"Bearer {admin_token}"}
            
            # test_1 create dataset in a scope which the member has access to
            ds1 = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                        name = "ds1", creator="standard1", keywords=[], ranking=0,
                        scope_uuid=scope1)
            response = client.post("/api/v2/dataset/", json=jsonable_encoder(ds1), headers=standard2_headers)
            self.assertEqual(response.status_code, 403)
            # test_2 create dataset in a scope which the member has no access to
            ds2 = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                        name = "ds2", creator="standard1", keywords=[], ranking=0,
                        scope_uuid=scope2)
            response = client.post("/api/v2/dataset/", json=jsonable_encoder(ds2), headers=standard2_headers)
            self.assertEqual(response.status_code, 201)
            # TODO this is the current behavoir, the question is a bit what the wanted behavior is.
            # test_3 create dataset in a scope, but as an admin (not added explicitely).
            ds3 = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                        name = "ds3", creator="standard1", keywords=[], ranking=0,
                        scope_uuid=scope2)
            response = client.post("/api/v2/dataset/", json=jsonable_encoder(ds3), headers=admin_headers)
            self.assertEqual(response.status_code, 201)
            
            # test access and search for standard user 2 (only access to 1 scope)
            datasetSearch1 = DatasetSearch()
            response = client.post("/api/v2/datasets/search/",
                                    json=jsonable_encoder(datasetSearch1), headers=standard2_headers)
            self.assertEqual(len(response.json()), 3)

            # test access and search for standard user 2, try to access scope where the user has no privileges to.
            datasetSearch1 = DatasetSearch(scope_uuids=[scope1])
            response = client.post("/api/v2/datasets/search/",
                                    json=jsonable_encoder(datasetSearch1), headers=standard2_headers)
            self.assertEqual(response.status_code, 403)
            
            # test access and search for admin user -- has access to all.
            datasetSearch1 = DatasetSearch(scope_uuids=[scope1, scope2])
            response = client.post("/api/v2/datasets/search/",
                                    json=jsonable_encoder(datasetSearch1), headers=admin_headers)
            self.assertEqual(len(response.json()), 4)
            
            # test access and search for admin user -- has access to all.
            datasetSearch1 = DatasetSearch()
            response = client.post("/api/v2/datasets/search/",
                                    json=jsonable_encoder(datasetSearch1), headers=admin_headers)
            self.assertEqual(len(response.json()), 4)

def _login_user(client, username, passwd):
    data = {"grant_type": "password",
            "username": username,
            "password": passwd}
    
    response = client.post("/api/v2/token", data=data)
    response_data = response.json()

    return response_data['access_token']

def _create_test_scenario(client, superusertoken):
    '''
    Creates users :
    admin
    scope_admin1
    scope_admin1
    
    standard1
    standard2
    
    create scopes : 
    scope1 : scope_admin1, standard1
    scope1 : scope_admin1, scope_admin2, standard1, standard2
    
    create dataset:
    ds1 : scope1
    ds2 : scope2
    '''
    headers = {"Authorization": f"Bearer {superusertoken}"}
    admin = UserCreate(username="admin", password="admin",
                        firstname="test", lastname="test", 
                        email="admin@test.com", user_type=UserType.admin)
    response =client.post("/api/v2/user", json=jsonable_encoder(admin), headers=headers)    

    scope_admin1 = UserCreate(username="scope_admin1", password="scope_admin1",
                        firstname="test", lastname="test", 
                        email="scope_admin1@test.com", user_type=UserType.scope_admin)
    response = client.post("/api/v2/user", json=jsonable_encoder(scope_admin1), headers=headers)    

    scope_admin2 = UserCreate(username="scope_admin2", password="scope_admin2",
                        firstname="test", lastname="test", 
                        email="scope_admin2@test.com", user_type=UserType.scope_admin)
    client.post("/api/v2/user", json=jsonable_encoder(scope_admin2), headers=headers)    

    standard1 = UserCreate(username="standard1", password="standard1",
                        firstname="test", lastname="test", 
                        email="standard1@test.com", user_type=UserType.standard_user)
    client.post("/api/v2/user", json=jsonable_encoder(standard1), headers=headers)    

    standard2 = UserCreate(username="standard2", password="standard2",
                        firstname="test", lastname="test", 
                        email="standard2@test.com", user_type=UserType.standard_user)
    client.post("/api/v2/user", json=jsonable_encoder(standard2), headers=headers)    
    
    # log in as scope_admin to create the scopes:
    scope_admin_token = _login_user(client, "scope_admin1", "scope_admin1")
    headers = {"Authorization": f"Bearer {scope_admin_token}"}

    # create and populate scopes:
    scope1 = ScopeCreate(name="scope1", uuid=uuid.uuid4(), description="")
    client.post("/api/v2/scope", json=jsonable_encoder(scope1), headers=headers)    

    scope2 = ScopeCreate(name="scope2", uuid=uuid.uuid4(), description="")
    client.post("/api/v2/scope", json=jsonable_encoder(scope2), headers=headers)    
    
    params = {"scope_uuid": str(scope1.uuid),
            "username": "standard1"}
    response = client.put("/api/v2/scope/assign_members", headers=headers, params=params)   


    params["scope_uuid"] = scope2.uuid
    client.put("/api/v2/scope/assign_members", headers=headers, params=params)  
    
    params["username"] = "standard2"
    client.put("/api/v2/scope/assign_members", headers=headers, params=params)   
    
    params["username"] = "scope2"
    client.put("/api/v2/scope/assign_members", headers=headers, params=params)    

    # create dummy dataset in each scope: 
    ds1 = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                        name = "ds1", creator="scopeadmin1", keywords=[], ranking=0,
                        scope_uuid=scope1.uuid)
    response = client.post("/api/v2/dataset/", json=jsonable_encoder(ds1), headers=headers)

    ds2 = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                        name = "ds2", creator="scopeadmin1", keywords=[], ranking=0,
                        scope_uuid=scope2.uuid)
    response = client.post("/api/v2/dataset/", json=jsonable_encoder(ds2), headers=headers)

    return [scope1.uuid, scope2.uuid]

if __name__ == '__main__':
    unittest.main() 
