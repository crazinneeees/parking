from rest_framework.permissions import BasePermission

from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == User.RoleType.ADMIN.value)