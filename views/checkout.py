from flask import Flask, Blueprint, request, jsonify
from jsonschemas.checkout import validate_stripe_charge
import sys
import stripe
from dotenv import load_dotenv
from os import getenv
from bson import ObjectId
from common.utils import *
from flask_pymongo import PyMongo
from common.db import mongo

load_dotenv()
checkout = Blueprint("checkout", __name__)


stripe_keys = {
    "secret_key": getenv("STRIPE_SECRET_KEY"),
    "publishable_key": getenv("STRIPE_PUBLISHABLE_KEY"),
}

stripe.api_key = stripe_keys["secret_key"]


@checkout.route("/charge", methods=["POST"])
def charge():
    if request.method == "POST":
        output = defaultObject()
        data = request.get_json()
        data = validate_stripe_charge(data)
        if data["ok"]:
            data = data["data"]
            total = 0

            for item in data["items"]:
                product = mongo.db.products.find_one({"_id": ObjectId(item["_id"])})
                product_price = item["quantity"] * product["price"]
                total += product_price

                if item["quantity"] > product["stock"]:
                    output["message"] = "NO_ENOUGH_STOCK"
                    return jsonify(output), 400

            customers = stripe.Customer.list(email=data["customer"]["email"])

            if len(customers.data) <= 0:
                customer = stripe.Customer.create(
                    email=data["customer"]["email"], source=data["customer"]["source"]
                )

            else:
                customer = customers.data[0]

            try:
                response = stripe.Charge.create(
                    amount=total,
                    currency="mxn",
                    description=data["description"],
                    customer=customer.id,
                )
                output["data"] = customer
                output["response"] = response
                output["status"] = 200
            except stripe.error.CardError as e:
                output["satus"] = 500
                output["message"] = e.error.message
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                output["satus"] = 401
                output["message"] = e.error.message
            except Exception as e:
                # Something else happened, completely unrelated to Stripe
                output["satus"] = 500
                output["message"] = e.error.message

            pass

            return jsonify(output)
