from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

products_post = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "description": {
            "type": "string"
        },
        "shippable": {
            "type": "boolean",
        },
        "price": {
            "type": "number",
        },
        "stock": {
            "type": "number",
        },
        "image": {
            "type": "string",
        }
    },
    "required": ["name", "description", "shippable", "price", "stock", "image"]
}

products_put = {
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
        },
        "available": {
            "type": "boolean",
        },
        "name": {
            "type": "string",
        },
        "description": {
            "type": "string"
        },
        "shippable": {
            "type": "boolean",
        },
        "price": {
            "type": "number",
        },
        "stock": {
            "type": "number",
        },
        "image": {
            "type": "string",
        }
    },
    "required": ["_id", "available", "name", "description", "shippable", "price", "stock", "image"]
}

just_id = {
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
        }
    },
    "required": ["_id"]
}


def validate_products_post(data):
    try:
        validate(data, products_post)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_products_put(data):
    try:
        validate(data, products_put)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_just_id(data):
    try:
        validate(data, just_id)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
