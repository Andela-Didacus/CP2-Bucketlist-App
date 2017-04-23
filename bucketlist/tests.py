import unittest
import json

from app import app, db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app_context().push()
        self.client = app.test_client()
        db.create_all()
        db.session.commit()
        test_bucketlist = {
            "name": "SOFA",
            "created by": 12,
            "items": [{
                "name":"eat chips",
                "done":"False"
            }]
        }
        self.client.post("/bucketlist/", data=json.dumps(test_bucketlist))

        test_user = {
           "first name":"didacus",
            "last name":"aseey",
            "gender":"Male",
            "username":"didah",
            "password":"pass",
            "email":"aseey@test.com"
        }
        self.client.post("/auth/register", data=json.dumps(test_user))

    def test_get_bucketlists(self):
        response = self.client.get("/bucketlist/")
        self.assertEqual(response.status_code, 200)

    def test_verification_required(self):
        response = self.client.get('/tokens')
        self.assertEqual(response.status_code, 401)
    
    def test_add_bucketlist(self):
        bucketlist = {
            "name": "SOFA",
            "created by": 12,
            "items": [{
                "name":"eat chips",
                "done":"False"
            }]
        }
        response = self.client.post("/bucketlist/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist(self):
        update_bucketlist = {
            "name": "sleep"
        }
        response = self.client.put("/bucketlist/1/", data=json.dumps(update_bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        response = self.client.delete("/bucketlist/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_single_bucketlist(self):
        response = self.client.get("/bucketlist/1/")
        self.assertEqual(response.status_code, 200)

    def test_user_regitration(self):
        new_user = {
           "first name":"didacus",
            "last name":"aseey",
            "gender":"Male",
            "username":"didah",
            "password":"pass",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(new_user))
        self.assertEqual(response.status_code, 201)

    def test_view_all_users(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)

    def test_get_single_user(self):
        response = self.client.get("/users/1/")
        self.assertEqual(response.status_code, 200)

    def test_edit_user(self):
        edited_user = {
            "first name":"test",
            "email": "email@gmail.com"
        }
        response = self.client.put('/users/1/', data=json.dumps(edited_user))
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.delete('/users/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_items(self):
        response = self.client.get('/bucketlists/1/items/')
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        new_item = {
           "name":"test project",
           "done":"False"
        }
        response = self.client.post('/bucketlists/1/items/', data=json.dumps(new_item))
        self.assertEqual(response.status_code, 201)

    def test_view_single_item(self):
        response = self.client.get('/bucketlists/1/items/1/')
        self.assertEqual(response.status_code, 200)

    def test_edit_item(self):
        edited_item = {
            "name":"finish work",
            "done": "true"
        }
        response = self.client.put('/bucketlists/1/items/1/', data=json.dumps(edited_item))
        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        response = self.client.delete('/bucketlists/1/items/1/')
        self.assertEqual(response.status_code, 200)

    def test_user_registration_without_first_name(self):
        test_user = {
            "last name":"aseey",
            "gender":"Male",
            "username":"didah",
            "password":"pass",
            "email":"aseey@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 400)
    
    def test_user_registration_with_duplicate_username(self):
        test_user = {
            "first name":"denis",
            "last name":"jambo",
            "gender":"Male",
            "username":"didah",
            "password":"psword",
            "email":"abel@test.com"
        }
        response = self.client.post("/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 400)

    def test_add_bucketlist_without_name(self):
        bucketlist = {
            "created by": 12,
            "items": [{
            "name":"eat chips",
            "done":"False"
            }]
        }
        response = self.client.post("/bucketlist/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 400)

    def test_add_bucketlist_without_items(self):
        bucketlist = {
            "created by": 12,
            "items": []
        }
        response = self.client.post("/bucketlist/", data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 201)

    def test_view_unavailable_user(self):
        response = self.client.get("/users/1000/")
        self.assertEqual(response.status_code, 500)

    def test_view_unavailable_bucketlist(self):
        response = self.client.get("/bucketlist/1000/")
        self.assertEqual(response.status_code, 500)

    def test_view_unavailable_item(self):
        response = self.client.get('/bucketlists/1/items/1000/')
        self.assertEqual(response.status_code, 500)
    
    def test_view_unavailable_bucketlist_items(self):
        response = self.client.get('/bucketlists/1000/items')
        self.assertEqual(response.status_code, 500)

if __name__=='__main__':
    unittest.main()  