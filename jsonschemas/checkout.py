from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

stripe_charge = {
    "type": "object",
    "properties": {
        "amount": {
            "type": "number"
        },
        "customer": {
            "type": "object",
            "email": {
                "type": "string"
            },
            "source": {
                "type": "string"
            }
        },
        "description": {
            "type": "string"
        }
    },

    "required": ["amount", "customer"]
}


def validate_stripe_charge(data):
    try:
        validate(data, stripe_charge)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
