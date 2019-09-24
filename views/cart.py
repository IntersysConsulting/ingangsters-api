# Import flask and necesary dependencies.
from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

from common.db import mongo
from common.utils import *
from jsonschemas.cart import validate_cart_create, validate_cart_add_product
from datetime import datetime
from bson import ObjectId

# Create the blueprint
cart = Blueprint('cart', __name__)

# POST cart
@cart.route('/cart', methods=['POST'])
@jwt_required
def cart_create():
    if request.method == 'POST':

        output = defaultObject()
        data = request.get_json()
        data = validate_cart_create(data)
        current_user = get_jwt_identity()

        if data['ok']:

            data = data['data']

            # Check if cart exists
            search_user_cart = mongo.db.cart.find_one(
                {'user': ObjectId(current_user['_id'])})

            # Look for product
            #product = mongo.db.products.find_one({'_id': ObjectId(data['product_id'])})
            product = mongo.db.product.find_one(
                {'_id': ObjectId(data['product_id'])})

            # Validations
            if(product == None):
                output['message'] = 'PRODUCT_NOT_FOUND'
                return jsonify(output), 404

            if(data['quantity'] > product['stock']):
                output['message'] = 'NO_ENOUGH_STOCK'
                return jsonify(output), 404

            if(data['price'] != product['price']):
                output['message'] = 'PRICE_MISMATCH'
                return jsonify(output), 404

            if (search_user_cart):
                # Update Cart
                data["product_id"] = ObjectId(data['product_id'])
                mongo.db.cart.update_one({'user': ObjectId(current_user['_id'])}, {
                    '$push': {'items': data}})

                data['updatedAt'] = datetime.timestamp(datetime.now())
                mongo.db.cart.update_one({'user': ObjectId(current_user['_id'])}, {
                    '$set': {'updatedAt': data['updatedAt']}})

                output['status'] = True
                output['message'] = 'CART_UPDATED'

            else:
                # Create Cart
                newCart = {}
                newCart['user'] = ObjectId(current_user['_id'])
                data["product_id"] = ObjectId(data['product_id'])
                data["price"] = data['price']
                data["quantity"] = data['quantity']
                newCart['items'] = [{"product_id": data["product_id"],
                                     "price": data["price"], "quantity": data["quantity"]}]

                newCart['createdAt'] = datetime.timestamp(datetime.now())
                newCart['updatedAt'] = datetime.timestamp(datetime.now())

                mongo.db.cart.insert_one(newCart)
                output['status'] = True
                output['message'] = 'CART_CREATED'

            return jsonify(output), 200
        else:
            output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
            return jsonify(output), 400
