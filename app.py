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
    print("BUCKET: " + getenv("AWS_BUCKET_NAME"))
    # Creates the app.
    app = Flask(__name__)
    CORS(app)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecomerce'
    #app.config['MONGO_URI'] = getenv("MONGO_URI")
    app.config['JWT_SECRET_KEY'] = getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = getenv("JWT_ACCESS_TOKEN_EXPIRES")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    jwt = JWTManager(app)

    from common.db import mongo
    mongo.init_app(app)

    from views.admins import admins
    from views.users import users
    from views.products import products
    from views.cart import cart
    app.register_blueprint(admins)
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    @app.route('/')
    def home():
        html = '<title>Hello ecommerce</title> <center><h1>Welcome</h1> <br> ecommerce Api Endpoint V2<center>'
        html += '<br> <a href="https://documenter.getpostman.com/view/8265028/SVfWN6UG?version=latest">Docs Here</a>'
        html += '<br> <a href="https://documenter.getpostman.com/view/8265028/SVfWN6UG?version=latest"><img src="https://images.g2crowd.com/uploads/product/image/social_landscape/social_landscape_fd527e1fc777d9e31b2a28e8d3c959a4/postman.jpg"></img></a>'
        return html, 200

    return app
