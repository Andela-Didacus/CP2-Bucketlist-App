import unittest
from flask import json

from app.models import User
from tests.test_base import BaseTestCase

class TestUserRegistrationAndLogin(BaseTestCase):

    def test_user_regitration(self):
        new_user = {
           "first name":"didacus",
            "last name":"aseey",
            "gender":"Male",
            "username":"aseey",
            "password":"didah",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_view_all_users(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = {
            "username": "test",
             "password": "test"
             }
        response = self.client.post("/auth/login", data=json.dumps(user), content_type="application/json")
        self.assertTrue(response.status_code, 200)
    
    def test_login_without_username(self):
        user = {
            "username":"",
            "passsword":"test"
        }
        response = self.client.post("/auth/login", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_login_without_password(self):
        user = {
            "username":"test",
            "password":""
        }
        response = self.client.post("/auth/login", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_login_without_credentials(self):
        user = {
            "username":"",
            "password":""
        }
        response = self.client.post("/auth/login", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_invalid_credentials(self):
        user = {
            "username":"aseey",
            "password":"aseeyffg"
        }
        response = self.client.post("/auth/login", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_user_registration_without_first_name(self):
        user = {
            "last name":"aseey",
            "gender":"Male",
            "username":"aseey",
            "password":"didah",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_without_last_name(self):
        user = {
            "first name":"didah",
            "gender":"Male",
            "username":"aseey",
            "password":"didah",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_without_username(self):
        user = {
            "firs name":"didah",
            "last name":"aseey",
            "gender":"Male",
            "password":"didah",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_without_password(self):
        user = {
            "firs name":"didah",
            "last name":"aseey",
            "gender":"Male",
            "username":"aseey",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_without_email(self):
        user = {
            "firs name":"didah",
            "last name":"aseey",
            "gender":"Male",
            "username":"aseey",
            "password":"didah"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_with_same_username(self):
        user = {
            "firs name":"test",
            "last name":"test",
            "gender":"test",
            "username":"test",
            "password":"test",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_user_with_same_email(self):
        user = {
            "firs name":"didah",
            "last name":"aseey",
            "gender":"Male",
            "username":"aseey",
            "password":"didah",
            "email":"test@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    # def test_get_single_user(self):
    #     self.user = db.session.query(User).filter_by(username="test").first()
    #     self.token = self.user.generate_auth_token().decode("ascii")

    #     response = self.client.get("/users/1/", headers={
    #         "Authorization": "Bearer {}".format(self.token)}))
    #     self.assertEqual(response.status_code, 200)

    # def test_edit_user(self):
    #     edited_user = {
    #         "first name":"test",
    #         "email": "email@gmail.com"
    #     }
    #     response = self.client.put('/users/1/', data=json.dumps(edited_user), content_type="application/json")
    #     self.assertEqual(response.status_code, 200)