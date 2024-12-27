from enum import Enum
from typing import List, Dict, Optional


class PermissionType(Enum):
    CUSTOM = "CUSTOM"
    TEMPLATE = "TEMPLATE"
    CUSTOM_TEMPLATE = "CUSTOM_TEMPLATE"


class User:
    def __init__(
        self,
        userId: str,
        userKeys: List[Dict[str, str]],
        userType: str,
        userLevel: str,
        permissionType: tuple,
        permissions: Dict[str, Optional[Dict[str, List[Dict[str, str]]]]],
    ):
        self.userId = userId
        self.userKeys = userKeys
        self.userType = userType
        self.userLevel = userLevel
        self.permissionType = permissionType
        self.permissions = permissions

    @staticmethod
    def fromDict(userId: str, data: Dict) -> "User":
        permissionType = tuple(PermissionType(pt) for pt in data["permission_type"])
        return User(
            userId=userId,
            userKeys=data["user_keys"],
            userType=data["user_type"],
            userLevel=data["user_level"],
            permissionType=permissionType,
            permissions=data["permissions"],
        )
