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


def validate_cart_create(data):
    try:
        validate(data, cart_create)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
