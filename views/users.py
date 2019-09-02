from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from common.db import mongo
from common.utils import *
from schemas.users import validate_user_login_credentials, validate_user_with_name, validate_user_patch_admin, validate_user_patch_user, validate_just_id
from datetime import datetime
from bson import ObjectId

users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        data = validate_user_login_credentials(data)
        output = defaultObject()
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            user_searched = mongo.db.users.find_one({'email': data['email']})
            if (user_searched and check_password_hash(user_searched['password'], data['password'])):
                del user_searched['password']
                del user_searched['createdAt']
                del user_searched['updatedAt']
                user_searched['_id'] = str(user_searched['_id'])
                user_searched['token'] = create_access_token(identity=user_searched)
                user_searched['refresh'] = create_refresh_token(identity=user_searched)
                output['status'] = True
                output['data'] = user_searched
                return jsonify(output), 200
            else:
                output['message'] = 'INVALID_CREDENTIALS'
                return jsonify(output), 404
        else:
            output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
            return jsonify(output), 400


@users.route('/signup', methods=['POST'])
def usersSignUp():
    if request.method == 'POST':
        output = defaultObject()
        data = request.get_json()
        data = validate_user_with_name(data)
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            user_searched = mongo.db.users.find_one({'email': data['email']})
            if (not user_searched):
                data['password'] = generate_password_hash(data['password']).decode('utf-8')
                data['role'] = 'USER'
                data['addresses'] = []
                data['createdAt'] = datetime.timestamp(datetime.now())
                data['updatedAt'] = datetime.timestamp(datetime.now())
                mongo.db.users.insert_one(data)
                output['status'] = True
                output['message'] = 'CORRECTLY_REGISTERED'
                return jsonify(output), 200
            else:
                output = defaultObject()
                output['message'] = 'USER_ALREADY_REGISTERED'  # Conflict
                return jsonify(output), 409
        else:
            output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
            return jsonify(output), 400


@users.route('/users', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required
def usersAdmin():
    output = defaultObject()
    current_user = get_jwt_identity()
    # print('Current user: ', current_user)
    if current_user['role'] == 'ADMIN':
        if request.method == 'GET':
            for single_user in mongo.db.users.find():
                single_user['_id'] = str(single_user['_id'])
                single_user['createdAt'] = convertTimestampToDateTime(single_user['createdAt'])
                single_user['updatedAt'] = convertTimestampToDateTime(single_user['updatedAt'])
                output['status'] = True
                output['data'].append(single_user)
            return jsonify(output), 200
        if request.method == 'PATCH':
            data = request.get_json()
            data = validate_user_patch_admin(data)
            if data['ok']:
                data = data['data']
                data['email'] = data['email'].lower()
                data['password'] = generate_password_hash(data['password']).decode('utf-8')
                user_updated = mongo.db.users.update_one({'_id': ObjectId(data['_id'])}, {'$set': {'email': data['email'], 'name': data['name'], 'password': data['password'], 'role': data['role']}})

                if (user_updated.modified_count):
                    output['status'] = True
                    output['message'] = 'UPDATED_CORRECTLY'
                    return jsonify(output), 200
                else:
                    output['message'] = 'USER_NOT_FOUND'
                    return jsonify(output), 404
        if request.method == 'DELETE':
            data = request.get_json()
            data = validate_just_id(data)
            if data['ok']:
                data = data['data']
                user_deleted = mongo.db.users.delete_one({'_id': ObjectId(data['_id'])})
                if (user_deleted.deleted_count):
                    output['status'] = True
                    output['message'] = 'DELETED_CORRECTLY'
                    return jsonify(output), 200
                else:
                    output['message'] = 'USER_NOT_FOUND'
                    return jsonify(output), 404
    else:
        output['status'] = False
        output['message'] = 'FORBIDDEN'
        return jsonify(output), 403


@users.route('/userupdate', methods=['PATCH'])
@jwt_required
def usersAll():
    output = defaultObject()
    current_user = get_jwt_identity()
    if request.method == 'PATCH':
        data = request.get_json()
        data = validate_user_patch_user(data)
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            search_email_user = mongo.db.users.find_one({'email': data['email']})
            if (not search_email_user):
                if (data['newpassword1'] == data['newpassword2']):
                    if (current_user['_id'] == data['_id']):
                        search_this_user = mongo.db.users.find_one({'_id': ObjectId(data['_id']), 'email': data['email']})
                        if (search_this_user and check_password_hash(search_this_user['password'], data['oldpassword'])):
                            data['password'] = generate_password_hash(data['oldpassword']).decode('utf-8')
                            user_updated = mongo.db.users.update_one({'_id': ObjectId(data['_id'])}, {'$set': {'email': data['email'], 'name': data['name'], 'password': data['password']}})
                            if (user_updated.modified_count):
                                output['status'] = True
                                output['message'] = 'UPDATED_CORRECTLY'
                                return jsonify(output), 200
                            else:
                                output['message'] = 'USER_NOT_FOUND'
                                return jsonify(output), 404
                        else:
                            output['message'] = 'INCORRECT_PASSWORD'
                            return jsonify(output), 409
                    else:
                        output['message'] = 'FORBIDDEN'
                        return jsonify(output), 403
                else:
                    output['message'] = 'NEW_PASSWORDS_NOT_MATCH'
                    return jsonify(output), 409
            else:
                output['message'] = 'EMAIL_ALREADY_IN_USE'
                return jsonify(output), 409
