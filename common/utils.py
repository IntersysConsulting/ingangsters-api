from flask import Flask, jsonify
from datetime import datetime
import json
import re

switcher = {
    "PENDING": [],
    "AWAITING_PAYMENT": [],
    "AWAITING_FULFILLMENT": [
        "MANUAL_VERIFICATION_REQUIRED",
        "REFUNDED",
        "PARTIALLY_REFUNDED",
        "AWAITING_SHIPMENT"
    ],
    "AWAITING_SHIPMENT": [
        "SHIPPED",
        "PARTIALLY_SHIPPED",
        "AWAITING_PICKUP",
    ],
    "SHIPPED": ["COMPLETED"],
    "PARTIALLY_SHIPPED": ["COMPLETED"],
    "AWAITING_PICKUP": ["COMPLETED"],
    "MANUAL_VERIFICATION_REQUIRED": ["AWAITING_FULFILLMENT"]
}

def convertTimestampToDateTime(timestamp):
    return datetime.fromtimestamp(int(re.findall("\d+", str(timestamp))[0]))


def defaultObject():
    output = '{"status":false,"message":"","data":[]}'
    return json.loads(output)


def defaultObjectDataAsAnObject():
    output = '{"status":false,"message":"","data":{}}'
    return json.loads(output)

def calculateFurtherStatus(currentStatus):
    return switcher.get(currentStatus, [])

def getStatusList():
    return list(switcher)