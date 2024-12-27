from abc import ABC, abstractmethod
from enum import Enum

# Enum for Permission Types
class PermissionType(Enum):
    CUSTOM = "CUSTOM"
    TEMPLATE = "TEMPLATE"
    CUSTOM_TEMPLATE = "CUSTOM_TEMPLATE"

# Abstract Base Class for Permission Handlers
class PermissionHandler(ABC):
    @abstractmethod
    def get_permissions(self, user, data, day, current_time):
        pass

# Custom Permission Handler
class CustomPermissionHandler(PermissionHandler):
    def get_permissions(self, user, data, day, current_time):
        return self._filter_permissions(user['permissions'].get('custom', {}).get(day, []), current_time)

    def _filter_permissions(self, permissions, current_time):
        return [
            permission
            for permission in permissions
            if self._is_time_in_range(
                permission['start_time'].split("T")[1].replace("Z", ""),
                permission['end_time'].split("T")[1].replace("Z", ""),
                current_time
            )
        ]

    @staticmethod
    def _is_time_in_range(start_time, end_time, current_time):
        return start_time <= current_time <= end_time

# Template Permission Handler
class TemplatePermissionHandler(PermissionHandler):
    def get_permissions(self, user, data, day, current_time):
        permissions = []
        template_ids = user['permissions'].get('template', [])
        for template_id in template_ids:
            template = data['templates'].get(template_id)
            if template:
                permissions.extend(self._filter_permissions(template['schedules'].get(day, []), current_time))
        return permissions

    def _filter_permissions(self, permissions, current_time):
        return [
            permission
            for permission in permissions
            if self._is_time_in_range(
                permission['start_time'].split("T")[1].replace("Z", ""),
                permission['end_time'].split("T")[1].replace("Z", ""),
                current_time
            )
        ]

    @staticmethod
    def _is_time_in_range(start_time, end_time, current_time):
        return start_time <= current_time <= end_time

# Custom + Template Permission Handler
class CustomTemplatePermissionHandler(PermissionHandler):
    def get_permissions(self, user, data, day, current_time):
        custom_handler = CustomPermissionHandler()
        template_handler = TemplatePermissionHandler()

        custom_permissions = custom_handler.get_permissions(user, data, day, current_time)
        template_permissions = template_handler.get_permissions(user, data, day, current_time)

        return custom_permissions + template_permissions
