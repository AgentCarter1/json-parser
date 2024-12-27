import json
from datetime import datetime, timezone
from permission_handler_factory import PermissionHandlerFactory

def load_json(file_path):
    """
    Load JSON data from a file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Main logic to retrieve permissions
def get_user_permissions(user_id, data, day):
    user = data['users'].get(user_id)
    if not user:
        return f"User with ID {user_id} not found."

    current_time = datetime.now(timezone.utc).strftime("%H:%M:%S")

    permission_type = user['permission_type']
    handler = PermissionHandlerFactory.get_handler(permission_type)

    return handler.get_permissions(user, data, day, current_time)

def main():
    # JSON file path
    file_path = "permissions.json"

    # Load the JSON data
    data = load_json(file_path)

    # Get current day in uppercase format
    current_day = datetime.now(timezone.utc).strftime("%A").upper()

    # Prompt user for a user ID
    user_id = input("Enter the user ID: ").strip()

    # Check permissions for the current day
    permissions = get_user_permissions(user_id, data, current_day)

    if isinstance(permissions, str):  # Error message
        print(permissions)
    elif permissions:
        print(f"User {user_id} has the following active permissions on {current_day}: {permissions}")
    else:
        print(f"User {user_id} has no active permissions on {current_day}.")

if __name__ == "__main__":
    main()
