from flask import json
from datetime import datetime
import unittest

from app import db
from app.models import User, Bucketlists, Items
from tests.test_base import BaseTestCase


class TestBucketList(BaseTestCase):

    def login_test_user(self):
        self.user = db.session.query(User).filter_by(username="test").first()
        self.token = self.user.generate_auth_token().decode("ascii")
        return self.token

    def create_test_bucketlist(self):
        self.token = self.login_test_user()
        bucketlist = {
            "name": "SOFA",
            "items": [{
                "name": "eat chips",
                "done": "False"
            }]
        }
        self.client.post("/bucketlists/", data=json.dumps(bucketlist), headers={
                         "Authorization": "Bearer " + self.token},
                         content_type="application/json")

    def test_verification_required(self):
        self.token = self.login_test_user()
        response = self.client.get('/bucketlists/')
        self.assertEqual(response.status_code, 401)

    def test_add_bucketlist(self):
        self.token = self.login_test_user()
        bucketlist = {
            "name": "SOFA",
            "items": [{
                "name": "eat chips",
                "done": "False"
            }]
        }
        response = self.client.post("/bucketlists/", data=json.dumps(bucketlist), headers={
                                    "Authorization": "Bearer " + self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_single_user(self):
        self.token = self.login_test_user()
        response = self.client.get(
            "/users/1", headers={"Authorization": "Bearer " + self.token})
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlists(self):
        self.token = self.login_test_user()
        response = self.client.get(
            "/bucketlists/", headers={"Authorization": "Bearer " + self.token})
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist(self):
        self.token = self.login_test_user()
        self.create_test_bucketlist()
        update_bucketlist = {
            "name": "sleep"
        }
        response = self.client.put("/bucketlists/1/", data=json.dumps(update_bucketlist), headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 202)

    def test_delete_bucketlist(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.delete(
            "/bucketlists/1/", headers={"Authorization": "Bearer " + self.token})
        self.assertEqual(response.status_code, 202)

    def test_view_single_bucketlist(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.get("/bucketlists/1/", headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_view_items(self):
        self.create_test_bucketlist()
        self.login_test_user()
        response = self.client.get('/bucketlists/1/items/', headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_view_single_item(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.get(
            '/bucketlists/1/items/1/', headers={"Authorization": "Bearer " + self.token})
        self.assertEqual(response.status_code, 200)

    def test_edit_item(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        edited_item = {
            "name": "finish work",
            "done": "true"
        }
        response = self.client.put('/bucketlists/1/items/1/', data=json.dumps(edited_item), headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 202)

    def test_delete_item(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.delete('/bucketlists/1/items/1/', headers={
                                      "Authorization": "Bearer " + self.token},
                                      content_type="application/json")
        self.assertEqual(response.status_code, 202)

    def test_add_bucketlist_without_name(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        bucketlist = {
            "created by": 12,
            "items": [{
                "name": "eat chips",
                "done": "False"
            }]
        }
        response = self.client.post("/bucketlists/", data=json.dumps(bucketlist), headers={
                                    "Authorization": "Bearer " + self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_add_bucketlist_without_items(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        bucketlist = {
            "name": "Test",
            "created by": 12
        }
        response = self.client.post("/bucketlists/", data=json.dumps(bucketlist), headers={
                                    "Authorization": "Bearer " + self.token},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_view_unavailable_item(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.get('/bucketlists/1/items/1000/',  headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_view_unavailable_bucketlist(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.get("/bucketlists/1000/",  headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_view_unavailable_bucketlist_items(self):
        self.create_test_bucketlist()
        self.token = self.login_test_user()
        response = self.client.get('/bucketlists/1000/items',  headers={
                                   "Authorization": "Bearer " + self.token},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 301)
