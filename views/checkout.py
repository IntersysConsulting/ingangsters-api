from flask import Flask, Blueprint, request, jsonify
from jsonschemas.checkout import validate_stripe_charge
import sys
import stripe
from dotenv import load_dotenv
from os import getenv
from bson import ObjectId
from common.utils import *

load_dotenv()
# Create the blueprint
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
            customer = stripe.Customer.create(
                email=data["customer"]["email"], source=data["customer"]["source"]
            )

            response = stripe.Charge.create(
                amount=data["amount"],
                currency="mxn",
                description=data["description"],
                customer=customer.id,
            )
            output["data"] = customer
            output["response"] = response

            return jsonify(output)
