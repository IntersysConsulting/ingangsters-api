from flask import Flask, jsonify
from datetime import datetime
import json
import re


def convertTimestampToDateTime(timestamp):
    return datetime.fromtimestamp(int(re.findall("\d+", str(timestamp))[0]))


def defaultObject():
    output = '{"status":false,"message":"","data":[]}'
    return json.loads(output)


def defaultObjectDataAsAnObject():
    output = '{"status":false,"message":"","data":{}}'
    return json.loads(output)
