from flask import request, jsonify, make_response, abort, url_for, abort, g
from flask_httpauth import HTTPTokenAuth
import json

import datetime
import time

from app import app, db
from app.models import Items, Bucketlists, User

db.create_all()
db.session.commit()
auth = HTTPTokenAuth(scheme="Bearer")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Page Not Found'}), 404)


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'Error': 'Method Not Allowed In this URI'}), 405)


@app.errorhandler(500)
def object_not_available(error):
    return make_response(jsonify({'Error': 'oops! sorry something went wrong try again later'}), 500)


@app.errorhandler(401)
def unauthorised_access(error):
    return make_response(jsonify({'Error': 'Need to login to access this page'}), 401)


@app.errorhandler(403)
def authentication_credentials_needed(error):
    return make_response(jsonify({"message": "login credentials required to proceed"}), 403)


@auth.verify_token
def verify_auth_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    if user:
        g.user = db.session.query(User).filter_by(id=user).first()
        print(g.user)
        return True


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


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
    if (username is None or password is None) or (first_name is None or last_name is None):  # missing parameters
        abort(400)
    # cant register user with same username
    if db.session.query(User).filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    user.first_name = first_name
    user.last_name = last_name
    user.gender = gender
    user.email = email
    user.timestamp = timestamp
    db.session.add(user)
    db.session.commit()
    return jsonify({'first name': user.first_name,
                    'last name': user.last_name,
                    'gender': user.gender,
                    'username': user.username,
                    'email': user.email
                    }), 201


@app.route('/auth/register/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username}), 200


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if not password or not username:
        return jsonify({"message": "username and password required to login"}), 400
    user = db.session.query(User).filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return jsonify({"message": "Sorry, Incorrect username and password combination"}), 403
    user_token = user.generate_auth_token()
    return json.dumps({"token": user_token.decode("ascii"), "id": user.id})


@app.route('/users/', methods=['GET'])
def getUsers():
    return getAllUsers()


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def userFunction(id):
    if request.method == 'GET':
        return getUser(id)
    elif request.method == 'DELETE':
        return deleteUser(id)
    elif request.method == 'PUT':
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        gender = request.json.get('gender')
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        return editUser(id, first_name, last_name, gender, username, password, email)


@app.route('/')
@app.route('/bucketlists/', methods=['GET', 'POST'])
@auth.login_required
def bucketlistsFunction():
    if request.method == 'GET':
        return getAllBucketlists(g.user.id)
    elif request.method == 'POST':
        name = request.json.get('name')
        created_by = request.json.get('created_by')
        items = request.json.get('items')
        created_by = g.user.id
        if not name or not created_by:
            abort(400)
        return addNewBucketlist(name, created_by, items)


@app.route('/bucketlists/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def singleBucketlist(id):
    if request.method == 'GET':
        return getBucketlist(id, g.user.id)
    elif request.method == 'PUT':
        name = request.json.get('name')
        return updateBucketlist(id, name, g.user.id)
    elif request.method == 'DELETE':
        return deleteBucketlist(id, g.user.id)


@app.route('/bucketlists/<int:id>/items/', methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def bucketlistItems(id):
    if request.method == 'GET':
        return getAllItems(id, g.user.id)
    elif request.method == 'POST':
        name = request.json.get('name')
        done = request.json.get('done')
        return addBucketlistItem(id, name, done, g.user.id)
    elif request.method == 'DELETE':
        return deleteAllItems(id, g.user.id)


@app.route('/bucketlists/<int:id>/items/<int:item_id>/', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def itemFunction(id, item_id):
    if request.method == 'GET':
        return getItem(id, item_id, g.user.id)
    elif request.method == 'PUT':
        done = request.json.get('done')
        name = request.json.get('name')
        return updateItem(id, item_id, done, name, g.user.id)
    elif request.method == 'DELETE':
        return deleteItem(id, item_id, g.user.id)

# helper functions


def getAllUsers():
    users = db.session.query(User).all()
    return jsonify(users=[user.serialize for user in users]), 200


def deleteUser(id):
    user = db.session.query(User).filter_by(id=id).one()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "user successfully deleted"}), 202


def getUser(id):
    user = db.session.query(User).filter_by(id=id).one()
    return jsonify(user=user.serialize), 200


def editUser(id, first_name=None, last_name=None, gender=None, username=None, password=None, email=None):
    user = db.session.query(User).filter_by(id=id).one()
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if gender:
        user.gender = gender
    if username:
        user.username = username
    if password:
        user.hash_password(password)
    if email:
        user.email = email
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user details succesfully updated"}), 202


def getAllBucketlists(user_id):
    # try:
    bucketlists = db.session.query(Bucketlists).all()
    return jsonify(bucketlists=[i.serialize for i in bucketlists]), 200
    # except:
    # return jsonify({"message":"OOPS!! Sorry something went wrong please try
    # again later"}), 400


def getBucketlist(id, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        return jsonify(bucketlist=bucketlist.serialize), 200
    except:
        return jsonify({"message": "sorry bucketlist does not exist for user"}), 404


def updateBucketlist(id, name, user_id):
    try:
        day = time.time()
        date_modified = str(datetime.datetime.fromtimestamp(
            day).strftime("%y-%m-%d"))
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        if name:
            bucketlist.name = name
        bucketlist.date_modified = date_modified
        db.session.add(bucketlist)
        db.session.commit()
        return jsonify({"message": "bucketlist updated succesfully"}), 202
    except:
        return jsonify({"message": "sorry bucketlist does not exist for user"}), 404


def deleteBucketlist(id, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({"message": "Bucketlist succesfully deleted"}), 202
    except:
        return jsonify({"message": "sorry bucketlist does not exist for user"}), 404


def addNewBucketlist(name, user_id, items=[]):
    day = time.time()
    date_created = str(datetime.datetime.fromtimestamp(
        day).strftime("%y-%m-%d"))
    date_modified = date_created
    bucketlist = Bucketlists(name=name)
    bucketlist.name = name
    bucketlist.date_modified = date_modified
    bucketlist.date_created = date_created
    bucketlist.created_by = user_id
    db.session.add(bucketlist)
    db.session.commit()
    if items is None:
        items = []
    if len(items) > 0:
        for each in items:
            item = Items(name=name, bucketlist=bucketlist)
            item.name = each['name']
            item.date_created = date_created
            item.date_modified = date_modified
            item.done = each['done']
            db.session.add(item)
            db.session.commit()
    return jsonify({'bucketlist name': bucketlist.name,
                    'items': items,
                    'date created': bucketlist.date_created,
                    'created by': bucketlist.created_by}), 201


def getAllItems(id, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        if not bucketlist:
            abort(404)
        items = db.session.query(Items).filter_by(bucketlist_id=id).all()
        return jsonify(items=[i.serialize for i in items]), 200
    except:
        return jsonify({"message": "sorry Item does not exist"}), 404


def addBucketlistItem(id, name, done, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        day = time.time()
        date_created = str(datetime.datetime.fromtimestamp(
            day).strftime("%y-%m-%d"))
        item = Items(name=name)
        item.name = name
        item.bucketlist_id = id
        item.done = done
        item.date_created = date_created
        item.date_modified = date_created
        db.session.add(item)
        db.session.commit()
        return jsonify({'item name': item.name,
                        'date created': item.date_created,
                        'date modified': item.date_modified,
                        'done': item.done}), 201
    except:
        return jsonify({"message": "Sorry bucketlist does not exist"}), 404


def getItem(id, item_id, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        item = db.session.query(Items).filter_by(
            bucketlist_id=id, id=item_id).one()
        return jsonify(item=item.serialize), 200
    except:
        return jsonify({"message": "Sorry cannot access that item"}), 404


def updateItem(id, item_id, done, name, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        day = time.time()
        date_modified = str(datetime.datetime.fromtimestamp(
            day).strftime("%y-%m-%d"))
        item = db.session.query(Items).filter_by(
            bucketlist_id=id, id=item_id).one()
        if name:
            item.name = name
        if done:
            item.done = done
        item.date_modified = date_modified
        db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Item succesfully Updated"}), 202
    except:
        return jsonify({"message": "Sorry cannot access that item"}), 404


def deleteItem(id, item_id, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        item = db.session.query(Items).filter_by(
            bucketlist_id=id, id=item_id).one()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "item succesfully deleted"}), 202
    except:
        return jsonify({"message": "Sorry cannot access that item"}), 404


def deleteAllItems(id, user_id):
    try:
        bucketlist = db.session.query(Bucketlists).filter_by(
            created_by=user_id, id=id).one()
        items = db.session.query(Items).filter_by(bucketlist_id=id).all()
        for item in items:
            db.session.delete(item)
            db.session.commit()
        return jsonify({"message": "items succesfully deleted"}), 202
    except:
        return jsonify({"message": "Sorry cannot access that item"}), 404
