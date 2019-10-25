from flask import Flask, Blueprint, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)

from common.db import mongo
from common.utils import *
from jsonschemas.orders import validate_order_create_data
from datetime import datetime
from bson import ObjectId

orders = Blueprint('orders', __name__)


@orders.route('/orders/create', methods=['POST'])
def orders_create():
    if request.method == 'POST':
        output = defaultObject()
        data = request.get_json()
        data = validate_order_create_data(data)
        if data['ok']:
            data = data['data']
            newArrayItems = []

            total_price = 0
            for single_item in data['items']:
                total_price += single_item['price'] * single_item['quantity']
                single_product_searched = mongo.db.products.find_one(
                    {'_id': ObjectId(single_item['_id'])})
                if (single_product_searched['price'] != single_item['price']):
                    output['message'] = 'PRICE_MISMATCH'
                    return jsonify(output), 400
                if (single_product_searched['stock'] < single_item['quantity']):
                    output['message'] = 'STOCK_MISMATCH'
                    return jsonify(output), 400
                single_item['image'] = single_product_searched['image']
                single_item['name'] = single_product_searched['name']
                newArrayItems.append(single_item)

            user = {'user': None, 'guest': None}
            if (data.get('userId')):
                search_user = mongo.db.users.find_one(
                    {'_id': ObjectId(data['userId'])})
                if search_user:
                    userData = {
                        '_id': data['userId'], 'name': search_user['name'], 'email': search_user['email']}
                    user['user'] = userData
                    cart_deleted = mongo.db.carts.delete_one(
                        {'user': ObjectId(data['userId'])})
            else:
                if (data.get('name') and data.get('email')):
                    user['guest'] = {'name': data['name'],
                                     'email': data['email']}
                else:
                    output['message'] = 'BAD_REQUEST'
                    return jsonify(output), 400

            order = {'user': user, 'shipping_address': data['shipping_address'], 'billing_address': data['billing_address'], 'items': newArrayItems,
                     'total': total_price, 'status': 'AWAITING_FULFILLMENT', 'createdAt': datetime.timestamp(datetime.now()), 'updatedAt': datetime.timestamp(datetime.now())}

            # Update stock
            for single_item in data['items']:
                single_product_searched = mongo.db.products.find_one(
                    {'_id': ObjectId(single_item['_id'])})
                newStock = single_product_searched['stock'] - \
                    single_item['quantity']

                updated_product = mongo.db.products.update_one(
                    {'_id': ObjectId(single_item['_id'])}, {'$set': {'stock': newStock}})

            new_order = mongo.db.orders.insert_one(order)
            output['data'] = str(new_order.inserted_id)
            output['status'] = True
            output['message'] = 'CORRECT'
            return jsonify(output), 200
        else:
            output['message'] = 'BAD_REQUEST: {}'.format(data['message'])
            return jsonify(output), 400


@orders.route('/order/<string:order_id>', methods=['GET'])
def get_order_byId(order_id):
    if request.method == 'GET':
        output = defaultObject()
        try:
            order = mongo.db.orders.find_one({'_id': ObjectId(order_id)})
            order['_id'] = str(order['_id'])
            order['createdAt'] = convertTimestampToDateTime(
                order['createdAt'])
            order['updatedAt'] = convertTimestampToDateTime(
                order['updatedAt'])
            output['data'] = order
            return jsonify(output), 200
        except:
            output['message'] = 'ORDER_NOT_FOUND'
            return jsonify(output), 404

@orders.route('/orders/list/<int:total_items>/<int:page>', methods=['GET'])
@jwt_required
def getPaginatedOrders(total_items, page):
    if request.method == 'GET':
        output = defaultObjectDataAsAnObject()
        current_user = get_jwt_identity()
        search_current_admin = mongo.db.admins.find_one(
            {'email': current_user['email']})
        if (search_current_admin):
            output['data']['total_orders'] = mongo.db.orders.count_documents({})
            ordersArray = []
            skip = (total_items * page) - total_items
            ordersList = mongo.db.orders.find().skip(skip).limit(total_items)
            for order in ordersList:
                del order['createdAt']
                del order['user']
                del order['shipping_address']
                del order['billing_address']
                order['_id'] = str(order['_id'])
                orderTotalDue = 0 
                for purchasedItem in order['items']:
                    orderTotalDue = orderTotalDue + (purchasedItem['price'] * purchasedItem['quantity'])
                order['total'] = orderTotalDue   
                order['date'] = datetime.fromtimestamp(int(order['updatedAt'])).strftime("%d/%m/%Y, %H:%M:%S")
                del order['items']
                order['next_status'] = calculateFurtherStatus(order['status'])
                ordersArray.append(order)
            output['data']['orders'] = ordersArray
            return jsonify(output),200
        else:
            output['message'] = "FORBIDDEN"
            output['status'] = False
            return jsonify(output), 403 
        
        
@orders.route('/orders/change/<string:orderId>/to/<string:newStatus>', methods=['POST'])
@jwt_required
def changeOrderStatus(orderId, newStatus):
    if request.method == 'POST':
        output = defaultObjectDataAsAnObject()
        current_user = get_jwt_identity()
        search_current_admin = mongo.db.admins.find_one(
            {'email': current_user['email']})
        if (search_current_admin):
            data = request.get_json() or  {"force": False}
            useForce = data.get('force', False)
            targetOrder = mongo.db.orders.find_one({"_id": ObjectId(orderId)})

            if(targetOrder):
                currentStatus = targetOrder['status']
                allowedNext = calculateFurtherStatus(currentStatus)
                if(newStatus in allowedNext or useForce):
                    updated_order = mongo.db.orders.update_one({'_id': ObjectId(targetOrder['_id'])}, {"$set": {
                        "status": newStatus
                    }})
                    if(updated_order.matched_count + updated_order.modified_count):
                        output['status'] = True
                        output['message'] = 'UPDATED_CORRECTLY'
                        return jsonify(output), 200
                else:
                    output['message'] = "INVALID_NEW_STATUS"
                    output['status'] = False
                    return jsonify(output), 400 
            else:
                output['message'] = "NOT_FOUND"
                output['status'] = False
                return jsonify(output), 404 
        else:
            output['message'] = "FORBIDDEN"
            output['status'] = False
            return jsonify(output), 403 