from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

from common.db import mongo
from common.utils import *
from jsonschemas.users import validate_user_login, validate_user_signup, validate_user_put_data, validate_user_put_password, validate_just_id
from datetime import datetime
from bson import ObjectId

users = Blueprint('users', __name__)


@users.route('/user/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        output = defaultObject()
        data = request.get_json()
        data = validate_user_login(data)
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            search_user = mongo.db.users.find_one({'email': data['email']})
            if (search_user and check_password_hash(search_user['password'], data['password'])):
                del search_user['password']
                search_user['_id'] = str(search_user['_id'])
                search_user['token'] = create_access_token(
                    identity=search_user)
                search_user['refresh'] = create_refresh_token(
                    identity=search_user)

                # Inserts cart data to current.
                user_cart = mongo.db.carts.find_one(
                    {'user': ObjectId(search_user['_id'])})

                if (user_cart):
                    if (data['cart']):
                        current_cart = user_cart['items']
                        new_items = data['cart']
                        new_current_cart = []
                        for new_item in new_items:
                            is_already_in_cart = False
                            new_item['_id'] = ObjectId(new_item['_id'])
                            searched_product = mongo.db.products.find_one(
                                {'_id': ObjectId(new_item['_id'])})
                            for item_in_cart in current_cart:
                                if(item_in_cart['_id'] == new_item['_id']):
                                    is_already_in_cart = True
                                    new_total_quantity = item_in_cart['quantity'] + \
                                        new_item['quantity']
                                    if(new_total_quantity <= searched_product['stock']):
                                        item_in_cart['quantity'] = new_total_quantity
                                        new_current_cart.append(item_in_cart)

                            if(not is_already_in_cart):
                                if(new_item['quantity'] > searched_product['stock']):
                                    new_item['quantity'] = searched_product['stock']
                                new_current_cart.append(new_item)

                        updated_cart = mongo.db.carts.update_one({'user': ObjectId(search_user['_id'])}, {
                                                                 '$set': {'items': new_current_cart}})
                        print("new data: ", new_items)
                        print("current cart: ", current_cart)
                        print("combination: ", new_current_cart)

                output['status'] = True
                output['data'] = search_user
                return jsonify(output), 200
            else:
                output['message'] = 'INVALID_CREDENTIALS'
                return jsonify(output), 404
        else:
            output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
            return jsonify(output), 400


@users.route('/user/signup', methods=['POST'])
def user_signup():
    if request.method == 'POST':
        output = defaultObject()
        data = request.get_json()
        data = validate_user_signup(data)
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            find_same_email_user = mongo.db.users.find_one(
                {'email': data['email']})
            if (not find_same_email_user):
                if (not data.get('phone')):
                    data['phone'] = None
                data['password'] = generate_password_hash(
                    data['password']).decode('utf-8')
                data['createdAt'] = datetime.timestamp(datetime.now())
                data['updatedAt'] = datetime.timestamp(datetime.now())
                data['addresses'] = []
                mongo.db.users.insert_one(data)
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


@users.route('/user', methods=['GET'])
@jwt_required
def get_user():
    if request.method == 'GET':
        output = defaultObject()
        current_user = get_jwt_identity()
        found_user = mongo.db.users.find_one(
            {'_id': ObjectId(current_user['_id'])})
        if (found_user):
            del found_user['password']
            found_user['_id'] = str(found_user['_id'])
            output['message'] = 'CORRECT'
            output['status'] = True
            output['data'] = found_user
            return jsonify(output), 200
        else:
            output['message'] = 'FORBIDDEN'
            return jsonify(found_user), 403


@users.route('/user/update', methods=['PUT'])
@jwt_required
def update_data_user():
    if request.method == 'PUT':
        output = defaultObject()
        current_user = get_jwt_identity()
        data = request.get_json()
        data = validate_user_put_data(data)
        if data['ok']:
            data = data['data']
            data['email'] = data['email'].lower()
            updateDict = {'email': data['email'], 'name': data['name']}
            if (data.get('phone')):
                updateDict["phone"] = data.get("phone")
            updateDict["addresses"] = []
            if (data.get('addresses')):
                updateDict["addresses"] = data.get("addresses")
            search_email_user = mongo.db.users.find_one(
                {'email': data['email']})
            if ((not search_email_user) or data['email'] == current_user['email']):
                user_updated = mongo.db.users.update_one(
                    {'_id': ObjectId(current_user['_id'])}, {'$set': updateDict})
                if (user_updated.modified_count + user_updated.matched_count):
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


@users.route('/user/changepassword', methods=['PUT'])
@jwt_required
def update_password_user():
    if request.method == 'PUT':
        output = defaultObject()
        current_user = get_jwt_identity()
        data = request.get_json()
        data = validate_user_put_password(data)
        if data['ok']:
            data = data['data']
            search_user_to_change = mongo.db.users.find_one(
                {'_id': ObjectId(current_user['_id'])})
            if (search_user_to_change and check_password_hash(search_user_to_change['password'], data['oldpassword'])):
                if (data['newpassword1'] == data['newpassword2']):
                    data['newpassword1'] = generate_password_hash(
                        data['newpassword1']).decode('utf-8')
                    data['updatedAt'] = datetime.timestamp(datetime.now())
                    update_user = mongo.db.users.update_one({'_id': ObjectId(current_user['_id'])}, {
                        '$set': {'password': data['newpassword1'], 'updatedAt': data['updatedAt']}})

                    if (update_user.modified_count):
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

# For Testing
@users.route('/user/delete', methods=['DELETE'])
@jwt_required
def delete_admin():
    if request.method == 'DELETE':
        output = defaultObject()
        current_user = get_jwt_identity()
        search_curent_user = mongo.db.users.find_one(
            {'email': current_user['email']})
        if (search_curent_user):
            user_deleted = mongo.db.users.delete_one(
                {'_id': ObjectId(search_curent_user['_id'])})
            if (user_deleted.deleted_count):
                output['status'] = True
                output['message'] = 'DELETED_CORRECTLY'
                return jsonify(output), 200
            else:
                output['message'] = 'USER_NOT_FOUND'
                return jsonify(output), 404
        else:
            output['message'] = 'FORBIDDEN'
            return jsonify(output), 403
