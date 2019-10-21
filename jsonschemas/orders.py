from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

order_create = {
    "type": "object",
    "properties": {
        "userId": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
        },
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "_id": {
                        "type": "string"
                    },
                    "price": {
                        "type": "number"
                    },
                    "quantity": {
                        "type": "number"
                    }
                },
                "required": ["_id", "price", "quantity"]
            }
        },
        "shipping_address": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string"
                },
                "state": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                },
                "zip": {
                    "type": "number"
                },
                "street": {
                    "type": "string"
                },
                "number": {
                    "type": "string"
                }
            },
            "required": ["country", "state", "city", "zip", "street", "number"]
        },
        "billing_address": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string"
                },
                "state": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                },
                "zip": {
                    "type": "number"
                },
                "street": {
                    "type": "string"
                },
                "number": {
                    "type": "string"
                }
            },
            "required": ["country", "state", "city", "zip", "street", "number"]
        }
    },
    "required": ["items", "shipping_address", "billing_address"]
}


def validate_order_create_data(data):
    try:
        validate(data, order_create)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
