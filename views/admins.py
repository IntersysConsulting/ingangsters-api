from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)

from common.db import mongo
from common.utils import *
from jsonschemas.admins import validate_admin_login, validate_admin_create, validate_admin_put_data, validate_admin_put_password, validate_just_id
from datetime import datetime
from bson import ObjectId

admins = Blueprint('admins', __name__)


@admins.route('/admin/create', methods=['POST'])
@jwt_required
def admin_create():
    if request.method == 'POST':
        output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_admin = mongo.db.admins.find_one({'email': current_user['email']})
        if (search_curent_admin):
            data = request.get_json()
            data = validate_admin_create(data)
            if data['ok']:
                data = data['data']
                data['email'] = data['email'].lower()
                find_same_email_admin = mongo.db.admins.find_one({'email': data['email']})
                if (not find_same_email_admin):
                    data['password'] = generate_password_hash(data['password']).decode('utf-8')
                    data['createdAt'] = datetime.timestamp(datetime.now())
                    data['updatedAt'] = datetime.timestamp(datetime.now())
                    mongo.db.admins.insert_one(data)
                    output['status'] = True
                    output['message'] = 'CORRECTLY_REGISTERED'
                    return jsonify(output), 200
                else:
                    output = defaultObject()
                    output['message'] = 'USER_ALREADY_REGISTERED'
                    return jsonify(output), 409
            else:
                output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
                return jsonify(output), 400


@admins.route('/admin/login', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        output = defaultObject()
        data = request.get_json()
        data = validate_admin_login(data)
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            search_admin = mongo.db.admins.find_one({'email': data['email']})
            if (search_admin and check_password_hash(search_admin['password'], data['password'])):
                del search_admin['password']
                search_admin['_id'] = str(search_admin['_id'])
                search_admin['token'] = create_access_token(identity=search_admin)
                search_admin['refresh'] = create_refresh_token(identity=search_admin)
                output['status'] = True
                output['data'] = search_admin
                return jsonify(output), 200
            else:
                output['message'] = 'INVALID_CREDENTIALS'
                return jsonify(output), 404
        else:
            output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
            return jsonify(output), 400


@admins.route('/admin/check', methods=['POST'])
@jwt_required
def check_admin_user():
    if request.method == 'POST':
        # output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_admin = mongo.db.admins.find_one({'email': current_user['email']})
        if (search_curent_admin):
            return jsonify({'isAdmin': True}), 200
        else:
            # output['message'] = 'FORBIDDEN'
            return jsonify({'isAdmin': False}), 403


@admins.route('/admin/users', methods=['GET'])
@jwt_required
def get_admins():
    if request.method == 'GET':
        output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_admin = mongo.db.admins.find_one({'email': current_user['email']})
        if (search_curent_admin):
            for single_user in mongo.db.admins.find():
                single_user['_id'] = str(single_user['_id'])
                single_user['createdAt'] = convertTimestampToDateTime(single_user['createdAt'])
                single_user['updatedAt'] = convertTimestampToDateTime(single_user['updatedAt'])
                output['status'] = True
                output['data'].append(single_user)
            return jsonify(output), 200
        else:
            output['message'] = 'FORBIDDEN'
            return jsonify(output), 403


@admins.route('/admin/update', methods=['PUT'])
@jwt_required
def update_data_admin():
    if request.method == 'PUT':
        output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_admin = mongo.db.admins.find_one({'email': current_user['email']})
        if (search_curent_admin):
            data = request.get_json()
            data = validate_admin_put_data(data)
            if data['ok']:
                data = data['data']
                data['email'] = data['email'].lower()
                search_email_user = mongo.db.users.find_one({'email': data['email']})
                if (not search_email_user):
                    data['updatedAt'] = datetime.timestamp(datetime.now())
                    admin_updated = mongo.db.admins.update_one({'_id': ObjectId(data['_id'])}, {'$set': {'email': data['email'], 'name': data['name'], 'updatedAt': data['updatedAt']}})

                    if (admin_updated.modified_count):
                        output['status'] = True
                        output['message'] = 'UPDATED_CORRECTLY'
                        return jsonify(output), 200
                    else:
                        output['message'] = 'USER_NOT_FOUND'
                        return jsonify(output), 404
                else:
                    output['message'] = 'EMAIL_ALREADY_IN_USE'
                    return jsonify(output), 409
            else:
                output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
                return jsonify(output), 400
        else:
            output['message'] = 'FORBIDDEN'
            return jsonify(output), 403


@admins.route('/admin/changepassword', methods=['PUT'])
@jwt_required
def update_password_admin():
    if request.method == 'PUT':
        output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_admin = mongo.db.admins.find_one({'email': current_user['email']})
        if (search_curent_admin):
            data = request.get_json()
            data = validate_admin_put_password(data)
            if data['ok']:
                data = data['data']
                search_admin_to_change = mongo.db.admins.find_one({'_id': ObjectId(data['_id'])})
                if (search_admin_to_change and check_password_hash(search_admin_to_change['password'], data['oldpassword'])):
                    if (data['newpassword1'] == data['newpassword2']):
                        data['newpassword1'] = generate_password_hash(data['newpassword1']).decode('utf-8')
                        update_admin = mongo.db.admins.update_one({'_id': ObjectId(data['_id'])}, {'$set': {'password': data['newpassword1'], 'updatedAt': data['updatedAt']}})

                        if (update_admin.modified_count):
                            output['status'] = True
                            output['message'] = 'UPDATED_CORRECTLY'
                            return jsonify(output), 200
                        else:
                            output['message'] = 'USER_NOT_FOUND'
                            return jsonify(output), 404
                    else:
                        output['message'] = 'PASSWORDS_NOT_MATCH'
                        return jsonify(output), 409
                else:
                    output['message'] = 'INCORRECT_PASSWORD'
                    return jsonify(output), 409
            else:
                output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
                return jsonify(output), 400
        else:
            output['message'] = 'FORBIDDEN'
            return jsonify(output), 403


@admins.route('/admin/delete', methods=['DELETE'])
@jwt_required
def delete_admin():
    if request.method == 'DELETE':
        output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_admin = mongo.db.admins.find_one({'email': current_user['email']})
        if (search_curent_admin):
            data = request.get_json()
            data = validate_just_id(data)
            if data['ok']:
                data = data['data']
                admin_deleted = mongo.db.admins.delete_one({'_id': ObjectId(data['_id'])})
                if (admin_deleted.deleted_count):
                    output['status'] = True
                    output['message'] = 'DELETED_CORRECTLY'
                    return jsonify(output), 200
                else:
                    output['message'] = 'USER_NOT_FOUND'
                    return jsonify(output), 404
            else:
                output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
                return jsonify(output), 400
        else:
            output['message'] = 'FORBIDDEN'
            return jsonify(output), 403
