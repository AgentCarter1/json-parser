from abc import ABC, abstractmethod
from datetime import datetime 
from models import User

class PermissionHandler(ABC):
    @abstractmethod
    def get_permissions(self, user: User, data: dict, day: str, current_time: int):
        pass

    @staticmethod
    def filter_permissions(permissions, current_time):
        return [
            permission
            for permission in permissions
            if PermissionHandler.is_time_in_range(
                permission["start_time"],
                permission["end_time"],
                current_time,
            )
        ]

    @staticmethod
    def is_time_in_range(start_time, end_time, current_time):
        start = datetime.utcfromtimestamp(start_time).time() 
        end = datetime.utcfromtimestamp(end_time).time()    
        current = datetime.utcfromtimestamp(current_time).time()  

        return start <= current <= end



class CustomPermissionHandler(PermissionHandler):
    def get_permissions(self, user: User, data: dict, day: str, current_time: int):
        permissions = user.permissions.get("custom", {}).get(day, [])
        return self.filter_permissions(permissions, current_time)


class TemplatePermissionHandler(PermissionHandler):
    def get_permissions(self, user: User, data: dict, day: str, current_time: int):
        permissions = []
        template_ids = user.permissions.get("template", [])
        for template_id in template_ids:
            template = data["templates"].get(template_id)
            if template:
                template_permissions = template["schedules"].get(day, [])
                permissions.extend(self.filter_permissions(template_permissions, current_time))
        return permissions


class CustomTemplatePermissionHandler(PermissionHandler):
    def get_permissions(self, user: User, data: dict, day: str, current_time: int):
        custom_handler = CustomPermissionHandler()
        template_handler = TemplatePermissionHandler()

        custom_permissions = custom_handler.get_permissions(
            user, data, day, current_time
        )
        template_permissions = template_handler.get_permissions(
            user, data, day, current_time
        )

        return custom_permissions + template_permissions
