# Import flask and necesary dependencies.
from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)
from common.db import mongo
from common.utils import *

# Create the blueprint
products = Blueprint('products', __name__)

# Create the route
@products.route('/products', methods=['GET'])
def productsAdmin():
    if request.method == 'GET':
        output = defaultObject()
        # output.append({'name': 'Martin'})
        for single_product in mongo.db.products.find():
            single_product['_id'] = str(single_product['_id'])
            single_product['createdAt'] = convertTimestampToDateTime(single_product['createdAt'])
            single_product['updatedAt'] = convertTimestampToDateTime(single_product['updatedAt'])
            output['data'].append(single_product)
        return jsonify(output), 200
