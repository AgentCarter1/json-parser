from permission_handler import (
    CustomPermissionHandler,
    TemplatePermissionHandler,
    CustomTemplatePermissionHandler,
)
from models import PermissionType


class PermissionHandlerFactory:
    HANDLERS = {
        (PermissionType.CUSTOM,): CustomPermissionHandler,
        (PermissionType.TEMPLATE,): TemplatePermissionHandler,
        (PermissionType.CUSTOM, PermissionType.TEMPLATE): CustomTemplatePermissionHandler,
        (PermissionType.TEMPLATE, PermissionType.CUSTOM): CustomTemplatePermissionHandler,
    }

    @staticmethod
    def get_handler(permission_type):
        permission_type_tuple = tuple(permission_type)
        handler_class = PermissionHandlerFactory.HANDLERS.get(permission_type_tuple)
        if handler_class:
            return handler_class()
        raise ValueError(f"Unknown permission type: {permission_type_tuple}")
