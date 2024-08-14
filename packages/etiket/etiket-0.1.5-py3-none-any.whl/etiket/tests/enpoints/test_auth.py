from fastapi.testclient import TestClient
from etiket.tests.set_up_testing_environment import *

from etiket.main import app
from etiket.settings import settings

import unittest, json

class test_authentication_endpoint(unittest.TestCase):
    def test_tokens(self):
        with TestClient(app) as client:
            # failed attempt at login
            data = {"grant_type": "password",
                    "username": settings.ETIKET_ADMIN_USERNAME,
                    "password": "faulty_password"}
            
            response = client.post("/api/v2/token", data=data)
            print(response.json())
            self.assertEqual(response.status_code, 401)
            
            # correct attempt at login
            data = {"grant_type": "password",
                    "username": settings.ETIKET_ADMIN_USERNAME,
                    "password": settings.ETIKET_ADMIN_PASSWORD}
            
            response = client.post("/api/v2/token", data=data)
            response_data = response.json()

            access_token = response_data["access_token"]
            refresh_token = response_data["refresh_token"]
            
            self.assertEqual(response.status_code, 200)
            
            self.assertNotEqual(response_data["access_token"], None)
            self.assertNotEqual(response_data["refresh_token"], None)
            self.assertNotEqual(response_data["refresh_token"], None)
            self.assertEqual(response_data["token_type"], "bearer")
            
            # ask a new access key
            data = {"grant_type" : "refresh_token",
                    "refresh_token": refresh_token}

            response = client.post("/api/v2/token", data=data)
            self.assertEqual(response.status_code, 200)

            response_data = response.json()
            new_access_token = response_data["access_token"]
            new_refresh_token = response_data["refresh_token"]
            
            # ask a ask with the old refresh token for a new access key
            data = {"grant_type" : "refresh_token",
                    "refresh_token": refresh_token}
            response = client.post("/api/v2/token", data=data)
            response_data = response.json()

            self.assertEqual(response.status_code, 401)
            
            # ask a ask with the new refresh token for a new access key (should be blocked)
            data = {"grant_type" : "refresh_token",
                    "refresh_token": new_refresh_token}
            response = client.post("/api/v2/token", data=data)
            response_data = response.json()

            self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 
