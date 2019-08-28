# Import flask and necesary dependencies.
from flask import Flask, Blueprint, request, jsonify

# Create the blueprint
products = Blueprint("products", __name__)

# Create the route
@products.route("/products", methods=["GET", "POST"])
def productB():
    return jsonify({"Hello": "Products"})
