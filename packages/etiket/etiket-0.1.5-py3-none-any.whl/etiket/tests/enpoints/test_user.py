from fastapi.testclient import TestClient
from etiket.tests.set_up_testing_environment import *

from etiket.main import app
from etiket.settings import settings

from etiket.db.data_models.user import UserCreate, UserUpdateMe
from etiket.db.types import UserType

from fastapi.encoders import jsonable_encoder
import unittest, json

class test_user_endpoint(unittest.TestCase):
    def test_user_creation(self):
        with TestClient(app) as client:
            # login as sudo user
            data = {"grant_type": "password",
                    "username": settings.ETIKET_ADMIN_USERNAME,
                    "password": settings.ETIKET_ADMIN_PASSWORD}
            
            response = client.post("/api/v2/token", data=data)
            response_data = response.json()

            sudo_access_token = response_data["access_token"]
            sudo_refresh_token = response_data["refresh_token"]
            
            self.assertEqual(response.status_code, 200)

            headers = {"Authorization": f"Bearer {sudo_access_token}"}
            
            # create a new standard user :
            user = UserCreate(username="standard", password="standard",
                                firstname="test", lastname="test", 
                                email="standard@test.com", user_type=UserType.standard_user)

            response = client.post("/api/v2/user", json=jsonable_encoder(user), headers=headers)
            self.assertEqual(response.status_code, 201)

            # FAIL when creating user with same name:
            user = UserCreate(username="standard", password="standard",
                                firstname="test", lastname="test", 
                                email="standard1@test.com", user_type=UserType.standard_user)

            response = client.post("/api/v2/user", json=jsonable_encoder(user), headers=headers)
            self.assertEqual(response.status_code, 409)

            # FAIL when creating user with same mail address:
            user = UserCreate(username="standard_", password="standard",
                                firstname="test", lastname="test", 
                                email="standard@test.com", user_type=UserType.standard_user)

            response = client.post("/api/v2/user", json=jsonable_encoder(user), headers=headers)
            self.assertEqual(response.status_code, 409)

            # create a new scope admin user :
            user = UserCreate(username="scope_admin", password="scope_admin",
                                firstname="test", lastname="test", 
                                email="scope_admin@test.com", user_type=UserType.standard_user)

            response = client.post("/api/v2/user", json=jsonable_encoder(user), headers=headers)
            self.assertEqual(response.status_code, 201)

            # create a new scope admin user :
            user = UserCreate(username="admin", password="admin",
                                firstname="test", lastname="test", 
                                email="admin@test.com", user_type=UserType.standard_user)

            response = client.post("/api/v2/user", json=jsonable_encoder(user), headers=headers)
            self.assertEqual(response.status_code, 201)

            # create a new admin user :
            user = UserCreate(username="superuser", firstname="test", lastname="test", password="superuser",
                              email="superuser@test.com", user_type=UserType.admin, disable_on=None)
            model_data = user.model_dump()
            model_data["user_type"] = UserType.superuser
            headers = {"Authorization": f"Bearer {sudo_access_token}"}
            response = client.post("/api/v2/user", json=jsonable_encoder(model_data), headers=headers)

            self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main() 
