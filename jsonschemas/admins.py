from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

admin_create = {
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
    "required": ["name", "email", "password"]
}

admin_login = {
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

admin_put_data = {
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "newpassword": {
            "type": "string"
        }
    },
    "required": ["_id", "name", "email"]
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

check_password = {
    "type": "object",
    "properties": {
        "password": {
            "type": "string",
        }
    },
    "required": ["password"]
}


def validate_admin_create(data):
    try:
        validate(data, admin_create)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_admin_login(data):
    try:
        validate(data, admin_login)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_admin_put_data(data):
    try:
        validate(data, admin_put_data)
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


def validate_just_password(data):
    try:
        validate(data, check_password)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
