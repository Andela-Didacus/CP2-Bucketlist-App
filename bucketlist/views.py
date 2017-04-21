from flask import request, jsonify, make_response, abort, url_for, abort

from models import Items, Bucketlists, User
from app import app, db

import datetime
import time

db.create_all()
db.session.commit()

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

@app.route('/auth/register/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@app.route('/')
@app.route('/bucketlists/', methods=['GET','POST'])
def bucketlistsFunction():
    if request.method == 'GET':
        return getAllBucketlists()
    elif request.method == 'POST':
        name = request.json.get('name')
        created_by = request.json.get('created_by')
        items = request.json.get('items')
        return addNewBucketlist(name, created_by, items)

@app.route('/bucketlists/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def singleBucketlist(id):
    if request.method == 'GET':
        return getBucketlist(id)
    elif request.method == 'PUT':
        name = request.json.get('name')
        return updateBucketlist(id, name)
    elif request.method == 'DELETE':
        return deleteBucketlist(id)

@app.route('/bucketlists/<int:id>/items/', methods=['GET', 'POST', 'DELETE'])
def bucketlistItems(id):
    if request.method == 'GET':
        return getAllItems(id)
    elif request.method == 'POST':
        name = request.json.get('name')
        done = request.json.get('done')
        return addBucketlistItem(id, name, done)
    elif request.method == 'DELETE':
        return deleteAllItems(id)

@app.route('/bucketlists/<int:id>/items/<int:item_id>/',methods=['GET','PUT','DELETE'])
def itemFunction(id, item_id):
    if request.method == 'GET':
        return getItem(id, item_id)
    elif request.method == 'PUT':
        done = request.json.get('done')
        name = request.json.get('name')
        return updateItem(id, item_id, done, name)
    elif request.method == 'DELETE':
        return deleteItem(id, item_id)
    

def getBucketlist(id):
    bucketlist = db.session.query(Bucketlists).filter_by(id = id).one()
    return jsonify(bucketlist=bucketlist.serialize) 

def updateBucketlist(id, name):
    day = time.time()
    date_modified = str(datetime.datetime.fromtimestamp(
        day).strftime("%y-%m-%d"))
    bucketlist = db.session.query(Bucketlists).filter_by(id = id).one()
    if name:
        bucketlist.name = name
    bucketlist.date_modified = date_modified
    db.session.add(bucketlist)
    db.session.commit()
    return getBucketlist(id)

def deleteBucketlist(id):
    bucketlist = db.session.query(Bucketlists).filter_by(id = id).one()
    db.session.delete(bucketlist)
    db.session.commit()
    return getAllBucketlists()

def getAllBucketlists():
    bucketlists = db.session.query(Bucketlists).all()
    return jsonify(bucketlists=[i.serialize for i in bucketlists])

def addNewBucketlist(name, user_id, items=[]):
    day = time.time()
    date_created = str(datetime.datetime.fromtimestamp(
        day).strftime("%y-%m-%d"))
    date_modified = date_created
    bucketlist = Bucketlists(name = name)
    bucketlist.name = name
    bucketlist.date_modified = date_modified
    bucketlist.date_created = date_created
    bucketlist.created_by = user_id
    db.session.add(bucketlist)
    db.session.commit()
    if len(items) > 0:
        for each in items:
            item = Items(name = name, bucketlist=bucketlist)
            item.name = each['name']
            item.date_created = date_created
            item.date_modified = date_modified
            item.done = each['done']
            db.session.add(item)
            db.session.commit()
    return jsonify({'bucketlist name': bucketlist.name,
                    'items':items,
                    'date created': bucketlist.date_created,
                    'created by': bucketlist.created_by}), 201

def getAllItems(id):
    items = db.session.query(Items).filter_by(bucketlist_id = id).all()
    return jsonify(items=[i.serialize for i in items])

def addBucketlistItem(id, name, done):
    day = time.time()
    date_created = str(datetime.datetime.fromtimestamp(
        day).strftime("%y-%m-%d"))
    item = Items(name = name)
    item.name = name
    item.bucketlist_id = id
    item.done = done
    item.date_created = date_created
    item.date_modified = date_created
    db.session.add(item)
    db.session.commit()
    return jsonify({'item name': item.name,
                    'date created': item.date_created,
                    'date modified':item.date_modified,
                    'done':item.done})

def getItem(id, item_id):
    item = db.session.query(Items).filter_by(bucketlist_id = id, id = item_id).one()
    return jsonify(item=item.serialize) 

def updateItem(id, item_id, done, name):
    day = time.time()
    date_modified = str(datetime.datetime.fromtimestamp(
        day).strftime("%y-%m-%d"))
    item = db.session.query(Items).filter_by(bucketlist_id = id, id = item_id).one()
    if name:
        item.name = name
    if done:
        item.done = done
    item.date_modified = date_modified
    db.session.add(item)
    db.session.commit()
    return getItem(id, item_id)

def deleteItem(id, item_id):
    item = db.session.query(Items).filter_by(bucketlist_id = id, id = item_id).one()
    db.session.delete(item)
    db.session.commit()
    return getAllItems(id)

def deleteAllItems(id):
    items = db.session.query(Items).filter_by(bucketlist_id = id).all()
    for item in items:
        db.session.delete(item)
        db.session.commit()
    return getAllItems(id)

if __name__=='__main__':
    app.run(debug=True)
