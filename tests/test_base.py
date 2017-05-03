import os
import unittest

from app import app, db
from app.models import User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        """ Default configuration. """
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            'sqlite:///' + os.path.join(basedir, 'test.db'))
        app.config["TESTING"] = True
        """ Update to use fixtures instead """
        db.drop_all()
        db.create_all()
        username = 'test'
        user = User(username=username)
        user.username = 'test'
        user.hash_password('test')
        user.first_name = 'admin'
        user.last_name = 'test'
        user.gender = 'male'
        user.email = 'test@test.com'
        user.timestamp = '1/1/1'
        db.session.add(user)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "main":
    unittest.main()
