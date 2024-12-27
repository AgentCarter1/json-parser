from enum import Enum
from typing import List, Dict, Optional


class PermissionType(Enum):
    CUSTOM = "CUSTOM"
    TEMPLATE = "TEMPLATE"
    CUSTOM_TEMPLATE = "CUSTOM_TEMPLATE"


class User:
    def __init__(
        self,
        user_id: str,
        user_keys: List[Dict[str, str]],
        user_type: str,
        user_level: str,
        permission_type: tuple,
        permissions: Dict[str, Optional[Dict[str, List[Dict[str, str]]]]],
    ):
        self.user_id = user_id
        self.user_keys = user_keys
        self.user_type = user_type
        self.user_level = user_level
        self.permission_type = permission_type
        self.permissions = permissions

    @staticmethod
    def from_dict(user_id: str, data: Dict) -> "User":
        permission_type = tuple(PermissionType(pt) for pt in data["permission_type"])
        return User(
            user_id=user_id,
            user_keys=data["user_keys"],
            user_type=data["user_type"],
            user_level=data["user_level"],
            permission_type=permission_type,
            permissions=data["permissions"],
        )
