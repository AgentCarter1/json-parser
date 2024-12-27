import json
from datetime import datetime, timezone
from permissionHandlerFactory import PermissionHandlerFactory
from models import User


def loadJson(filePath):
    with open(filePath, "r") as f:
        return json.load(f)


def getUserPermissions(userId, data, day):
    userData = data["users"].get(userId)
    if not userData:
        return f"User with ID {userId} not found."
    user = User.fromDict(userId, userData)
    currentTime = datetime.now(timezone.utc)
    handler = PermissionHandlerFactory.getHandler(user.permissionType)
    return handler.getPermissions(user, data, day, currentTime)


def main():
    filePath = "permissions.json"
    data = loadJson(filePath)
    currentDay = datetime.now(timezone.utc).strftime("%A").upper()
    userId = input("Enter the user ID: ").strip()
    permissions = getUserPermissions(userId, data, currentDay)
    
    if isinstance(permissions, str): 
        print(permissions)
    elif permissions:
        print(f"User {userId} has the following active permissions on {currentDay}: {permissions}")
    else:
        print(f"User {userId} has no active permissions on {currentDay}.")


if __name__ == "__main__":
    main()
