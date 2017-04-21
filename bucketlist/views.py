from flask import request, jsonify, make_response, abort, url_for, abort
from app import app, db

import datetime
import time

db.create_all()
db.commit()

@app.route('/auth/register', methods=['POST'])
def registerUser():
    day = time.time()
    timestamp = str(datetime.datetime.fromtimestamp(
        day).strftime("%y-%m-%d"))
    first_name = request.json.get('first name')
    last_name = request.json.get('last name')
    gender = request.json.get('gender')
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if (username is None or password is None) or (first_name is None or last_name is None): #missing parameters
        abort(400) 
    if db.session.query(User).filter_by(username = username).first() is not None: #cant register user with same username
        abort(400)
    user = User(username = username)
    user.hash_password(password)
    user.first_name = first_name
    user.last_name = last_name
    user.gender = gender
    user.email = email
    user.timestamp = timestamp
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'first name': user.first_name,
            'last name':user.last_name,
            'gender':user.gender,
            'email':user.email 
         }), 201

@app.route('/')
@app.route('/bucketlists/', methods=['GET','POST'])
def bucketlistsFunction():
    if request.method == 'GET':
        return getAllBucketlists()


def getAllBucketlists():
    bucketlists = db.session.query(Bucketlists).all()
    return jsonify(bucketlists=[i.serialize for i in bucketlists])

    