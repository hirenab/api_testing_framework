from jsonschema import validate, ValidationError

# schema for user creation response
create_user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "gender": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["id", "name", "email", "gender", "status"]
}

# schema for user update response
update_user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "gender": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["id", "name", "email", "gender", "status"]
}

# Function to validate a response against a schema
def validate_response(response_data, schema):
    try:
        validate(instance=response_data, schema=schema)
        return True
    except ValidationError as err:
        print(f"Schema validation error: {err}")
        return False
    