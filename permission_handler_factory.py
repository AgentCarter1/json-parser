from permission_handler import (
    CustomPermissionHandler,
    TemplatePermissionHandler,
    CustomTemplatePermissionHandler,
    PermissionType,
)

# Factory for Permission Handlers
class PermissionHandlerFactory:
    @staticmethod
    def get_handler(permission_type):
        if permission_type == [PermissionType.CUSTOM.value]:
            return CustomPermissionHandler()
        elif permission_type == [PermissionType.TEMPLATE.value]:
            return TemplatePermissionHandler()
        elif set(permission_type) == {PermissionType.CUSTOM.value, PermissionType.TEMPLATE.value}:
            return CustomTemplatePermissionHandler()
        raise ValueError(f"Unknown permission type: {permission_type}")
