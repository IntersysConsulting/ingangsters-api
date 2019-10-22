from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
import datetime
from dotenv import load_dotenv
from os import getenv


load_dotenv()


def create_app():
    print('BUCKET: ' + getenv('AWS_BUCKET_NAME'))
    # Creates the app.
    app = Flask(__name__)
    CORS(app)
    app.config['MONGO_URI'] = getenv('MONGO_URI')
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = getenv('JWT_ACCESS_TOKEN_EXPIRES')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    jwt = JWTManager(app)

    from common.db import mongo

    mongo.init_app(app)

    from views.admins import admins
    from views.users import users
    from views.products import products
    from views.cart import cart
    from views.orders import orders
    from views.checkout import checkout

    app.register_blueprint(admins)
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    app.register_blueprint(orders)
    app.register_blueprint(checkout)

    @app.route('/')
    def home():
        html = '<title>Hello ecommerce</title> <center><h1>Welcome</h1> <br> ecommerce Api Endpoint V2<center>'
        return html, 200

    return app
