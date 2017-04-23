from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
import random, string

from app import app, db

app.config.from_pyfile('config.cfg')
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

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

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })
    
    @staticmethod
    def verify_auth_token(token): 
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            #Valid Token, but expired
            return None
        except BadSignature:
            #Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'first name':self.first_name,
           'Last name':self.last_name,
           'gender':self.gender,
           'username':self.username,
           'email':self.email
        }

class Bucketlists(db.Model):
    __tablename_='bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable = False)
    date_created= db.Column('date_created', db.String(50))
    date_modified = db.Column('date_modified', db.String(50))
    created_by = db.Column('created_by', db.String(50))
    items = db.relationship('Items', backref='bucketlist', lazy='dynamic')

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       	   'id': self.id,
           'name': self.name,
           'date_created' : self.date_created,
           'created_by': self.created_by
       }

class Items(db.Model):
    __tablename_='Items'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    date_created= db.Column('date_created', db.String(50))
    date_modified = db.Column('date_modified', db.String(50))
    done = db.Column('done', db.String(50), nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'date created' : self.date_created,
           'date modified':self.date_modified,
           'done':self.done
       }

