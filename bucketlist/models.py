from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
import random, string

from app import app, db

app.config.from_pyfile('config.cfg')

class User(db.Model):
    __tablename__='Users'

    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(50), nullable=False)
    last_name = db.Column('last_name', db.String(50), nullable=False)
    gender = db.Column('Gender', db.String(20), nullable=False)
    timestamp = db.Column('timestamp', db.String(50), nullable=False)
    email = db.Column('email', db.String(50), nullable=False)
    username = db.Column('username', db.String(32), index=True)
    password_hash = db.Column('password_hash', db.String(64))
    bucketlists =  db.relationship('Bucketlists', backref='user', lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'first name':self.first_name,
           'Last name':self.last_name,
           'gender':self.gender,
           'username':self.gender,
           'email':self.email
        }

    