from jsonschema import validate

# Schema for a single user object
user_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    },
                    "required": ["lat", "lng"]
                }
            },
            "required": ["street", "suite", "city", "zipcode", "geo"]
        },
        "phone": {"type": "string"},
        "website": {"type": "string", "format": "uri"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"}
            },
            "required": ["name", "catchPhrase", "bs"]
        }
    },
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"]
}

# Schema for creating a new user (subset of user_schema)
create_user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    },
                    "required": ["lat", "lng"]
                }
            },
            "required": ["street", "suite", "city", "zipcode", "geo"]
        },
        "phone": {"type": "string"},
        "website": {"type": "string", "format": "uri"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"}
            },
            "required": ["name", "catchPhrase", "bs"]
        }
    },
    "required": ["name", "username", "email", "address", "phone", "website", "company"]
}

# Schema for updating a user (partial update)
update_user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    },
                    "required": ["lat", "lng"]
                }
            }
        },
        "phone": {"type": "string"},
        "website": {"type": "string", "format": "uri"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"}
            }
        }
    },
    "required": []  # No fields are required for an update (partial update)
}

# Schema for deleting a user
delete_user_schema = {
    "type": "object",
    "properties": {},  # No specific properties are required
    "required": []    # No fields are required
}

# Function to validate API responses
def validate_response(response_data, schema):
    try:
        validate(instance=response_data, schema=schema)
        return True
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False