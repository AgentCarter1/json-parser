import json
from datetime import datetime, timezone
from permission_handler_factory import PermissionHandlerFactory
from models import User


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def get_user_permissions(user_id, data, day):
    user_data = data["users"].get(user_id)
    if not user_data:
        return f"User with ID {user_id} not found."

    user = User.from_dict(user_id, user_data)

    current_time = datetime.now(timezone.utc)
    handler = PermissionHandlerFactory.get_handler(user.permission_type)

    return handler.get_permissions(user, data, day, current_time)


def main():
    file_path = "permissions.json"

    data = load_json(file_path)

    current_day = datetime.now(timezone.utc).strftime("%A").upper()

    user_id = input("Enter the user ID: ").strip()

    permissions = get_user_permissions(user_id, data, current_day)

    if isinstance(permissions, str): 
        print(permissions)
    elif permissions:
        print(f"User {user_id} has the following active permissions on {current_day}: {permissions}")
    else:
        print(f"User {user_id} has no active permissions on {current_day}.")


if __name__ == "__main__":
    main()
