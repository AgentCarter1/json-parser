from abc import ABC, abstractmethod
from datetime import datetime
from models import User


class PermissionHandler(ABC):
    @abstractmethod
    def getPermissions(self, user: User, data: dict, day: str, currentTime: datetime):
        pass

    @staticmethod
    def filterPermissions(permissions, currentTime):
        return [
            permission
            for permission in permissions
            if PermissionHandler.isTimeInRange(
                permission["start_time"],
                permission["end_time"],
                currentTime,
            )
        ]

    @staticmethod
    def isTimeInRange(startTime, endTime, currentTime):
        start = datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%SZ").time()
        end = datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%SZ").time()
        return start <= currentTime.time() <= end


class CustomPermissionHandler(PermissionHandler):
    def getPermissions(self, user: User, data: dict, day: str, currentTime: datetime):
        permissions = user.permissions.get("custom", {}).get(day, [])
        return self.filterPermissions(permissions, currentTime)


class TemplatePermissionHandler(PermissionHandler):
    def getPermissions(self, user: User, data: dict, day: str, currentTime: datetime):
        permissions = []
        templateIds = user.permissions.get("template", [])
        for templateId in templateIds:
            template = data["templates"].get(templateId)
            if template:
                permissions.extend(
                    self.filterPermissions(
                        template["schedules"].get(day, []), currentTime
                    )
                )
        return permissions


class CustomTemplatePermissionHandler(PermissionHandler):
    def getPermissions(self, user: User, data: dict, day: str, currentTime: datetime):
        customHandler = CustomPermissionHandler()
        templateHandler = TemplatePermissionHandler()

        customPermissions = customHandler.getPermissions(
            user, data, day, currentTime
        )
        templatePermissions = templateHandler.getPermissions(
            user, data, day, currentTime
        )

        return customPermissions + templatePermissions
