from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

user_signup = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
        },
        "phone": {
            "type": "string",
        }
    },
    "required": ["name", "email", "password"]
}

user_login = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
        }
    },
    "required": ["email", "password"]
}

user_put_data = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "addresses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["Billing", "Shipping", "Both"]
                    },
                    "alias": {
                        "type": "string"
                    },
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
                "required": ["alias", "country", "state", "city", "zip", "street", "number", "type"]
            }
        }
    },
    "required": ["name", "email"]
}

user_put_password = {
    "type": "object",
    "properties": {
        "oldpassword": {
            "type": "string",
        },
        "newpassword1": {
            "type": "string",
        },
        "newpassword2": {
            "type": "string",
        }
    },
    "required": ["oldpassword", "newpassword1", "newpassword2"]
}

check_id = {
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
        }
    },
    "required": ["_id"]
}


def validate_user_signup(data):
    try:
        validate(data, user_signup)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_login(data):
    try:
        validate(data, user_login)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_put_data(data):
    try:
        validate(data, user_put_data)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_put_password(data):
    try:
        validate(data, user_put_password)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_just_id(data):
    try:
        validate(data, check_id)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
