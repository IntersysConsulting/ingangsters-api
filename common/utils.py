from flask import Flask, jsonify
from datetime import datetime
import json
import re


def convertTimestampToDateTime(timestamp):
    return datetime.fromtimestamp(int(re.findall("\d+", str(timestamp))[0]))
    # single_user['createdAt'] = datetime.fromtimestamp(int(re.findall('\d+', str(single_user['createdAt']))[0]))  # Converts timestamp to Datetime.
    # single_user['updatedAt'] = datetime.fromtimestamp(int(re.findall('\d+', str(single_user['updatedAt']))[0]))


def defaultObject():
    output = '{"status":false,"message":"","data":[]}'
    return json.loads(output)
