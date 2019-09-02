from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
import datetime

# Add the blueprints, i.e, products from views
# from views.products import products
# from views.users import users

# from common.db import mongo


def create_app(config_filename):
    # Creates the app.
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/ecommerce'
    app.config['JWT_SECRET_KEY'] = 'secret_pass'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    jwt = JWTManager(app)
    #app.config['MONGO_URI'] = 'mongodb+srv://aintersys:aintersys@e-commerce-lcqki.mongodb.net/test?retryWrites=true&w=majority'
    #app.config['MONGO_URI'] = 'mongodb://aintersys:aintersys@e-commerce-shard-00-00-lcqki.mongodb.net:27017,e-commerce-shard-00-01-lcqki.mongodb.net:27017,e-commerce-shard-00-02-lcqki.mongodb.net:27017/test?ssl=true&replicaSet=e-commerce-shard-0&authSource=admin&retryWrites=true&w=majority'

    from common.db import mongo
    mongo.init_app(app)

    from views.products import products
    from views.users import users
    app.register_blueprint(products)
    app.register_blueprint(users)

    @app.route('/')
    def home():
        return '<title>Hello ecommerce</title> <center><h1>Welcome</h1> <br> ecommerce Api Endpoint V1<center>', 200

    return app

# app.config['JWT_SECRET_KEY'] = 'secret_pass'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
# mongo = PyMongo(app)
# jwt = JWTManager(app)
