from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

cart_create = {
    "type": "object",
    "properties": {
        "user": {
            "type": "string"
        },
        "items": {
            "type": "array",
            "items":{
                "type": "object",
                "properties":{
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
        }

    },
    "required": ["items"]
}

cart_productsSummary = {
    "type": "object",
    "properties":{
        "_ids": {
            "type": "array",
            "items":{
                "type": "string"
            }
        }
    },
    "required": ["_ids"]
}

def validate_cart_summary(data):
    try:
        validate(data,cart_productsSummary)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

def validate_cart_create(data):
    try:
        validate(data, cart_create)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
