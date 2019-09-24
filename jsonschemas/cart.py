from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

cart_create = {
    "type": "object",
    "properties": {
        "user": {
            "type": "string"
        },
        "product_id": {
            "type": "string"
        },
        "price": {
            "type": "number"
        },
        "quantity": {
            "type": "number"
        }
    },
    "required": ["product_id", "price", "quantity"]
}

cart_add_product = {
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
        },
        "products": {
            "type": "array",
            "items": {
                "product_id": {
                    "type": "string"
                },
                "price": {
                    "type": "number"
                },
                "quantity": {
                    "type": "number"
                }
            }
        }
    },
    "required": ["_id", "products"]
}


def validate_cart_create(data):
    try:
        validate(data, cart_create)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_cart_add_product(data):
    try:
        validate(data, cart_add_product)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
