from permissionHandler import (
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
    def getHandler(permissionType):
        permissionTypeTuple = tuple(permissionType)
        handlerClass = PermissionHandlerFactory.HANDLERS.get(permissionTypeTuple)
        if handlerClass:
            return handlerClass()
        raise ValueError(f"Unknown permission type: {permissionTypeTuple}")
