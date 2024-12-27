from abc import ABC, abstractmethod
from datetime import datetime
from models import User


class PermissionHandler(ABC):
    @abstractmethod
    def get_permissions(self, user: User, data: dict, day: str, current_time: datetime):
        pass

    @staticmethod
    def _filter_permissions(permissions, current_time):
        return [
            permission
            for permission in permissions
            if PermissionHandler._is_time_in_range(
                permission["start_time"],
                permission["end_time"],
                current_time,
            )
        ]

    @staticmethod
    def _is_time_in_range(start_time, end_time, current_time):
        start = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").time()
        end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ").time()
        return start <= current_time.time() <= end


class CustomPermissionHandler(PermissionHandler):
    def get_permissions(self, user: User, data: dict, day: str, current_time: datetime):
        permissions = user.permissions.get("custom", {}).get(day, [])
        return self._filter_permissions(permissions, current_time)


class TemplatePermissionHandler(PermissionHandler):
    def get_permissions(self, user: User, data: dict, day: str, current_time: datetime):
        permissions = []
        template_ids = user.permissions.get("template", [])
        for template_id in template_ids:
            template = data["templates"].get(template_id)
            if template:
                permissions.extend(
                    self._filter_permissions(
                        template["schedules"].get(day, []), current_time
                    )
                )
        return permissions


class CustomTemplatePermissionHandler(PermissionHandler):
    def get_permissions(self, user: User, data: dict, day: str, current_time: datetime):
        custom_handler = CustomPermissionHandler()
        template_handler = TemplatePermissionHandler()

        custom_permissions = custom_handler.get_permissions(
            user, data, day, current_time
        )
        template_permissions = template_handler.get_permissions(
            user, data, day, current_time
        )

        return custom_permissions + template_permissions
