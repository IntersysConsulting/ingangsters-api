from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

stripe_charge = {
    "type": "object",
    "properties": {
        "customer": {
            "type": "object",
            "email": {"type": "string"},
            "source": {"type": "string"},
        },
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "_id": {"type": "string"},
                    "price": {"type": "number"},
                    "quantity": {"type": "number"},
                },
                "required": ["_id", "price", "quantity"],
            },
        },
        "description": {"type": "string"},
    },
    "required": ["items", "customer"],
}


def validate_stripe_charge(data):
    try:
        validate(data, stripe_charge)
    except ValidationError as e:
        return {"ok": False, "message": e}
    except SchemaError as e:
        return {"ok": False, "message": e}
    return {"ok": True, "data": data}
