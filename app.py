from flask import Flask
#Add the blueprints, i., products from views
from views.products import products

#Creates the app and register the blueprint
app = Flask(__name__)
app.register_blueprint(products)

@app.route("/")
def home():
    return "<title>Hello ecommerce</title> <center><h1>Welcome</h1> <br> ecommerce Api Endpoint V1<center>"