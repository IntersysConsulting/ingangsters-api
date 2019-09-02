from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

user_schema = {
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

user_schema_login = {
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

user_patch_admin = {
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
        "password": {
            "type": "string",
        },
        "role": {
            "type": "string",
        }
    },
    "required": ["_id", "name", "email", "password", "role"]
}

user_patch_user = {
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
    "required": ["_id", "name", "email", "oldpassword", "newpassword1", "newpassword2"]
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


def validate_user_with_name(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_login_credentials(data):
    try:
        validate(data, user_schema_login)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_patch_admin(data):
    try:
        validate(data, user_patch_admin)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}


def validate_user_patch_user(data):
    try:
        validate(data, user_patch_user)
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
