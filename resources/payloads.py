import time

# Payload for creating a user
create_user_payload = {
    "name": "Hiren AB",
    "email": f"hiren_{int(time.time())}@example.com",  # Generate unique email
    "gender": "male",
    "status": "active"
}

# Payload for updating a user
update_user_payload = {
    "name": "Hiren AB Updated",
    "email": f"hirenab_{int(time.time())}@example.com",  # Updated email
    "status": "inactive"
}
