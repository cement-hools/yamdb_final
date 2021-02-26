from rest_framework import permissions

from .models import Roles


class IsAdmin(permissions.BasePermission):
    """Права роли admin."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(
                (request.user.role == Roles.ADMIN)
                or (request.user.is_staff and request.user.is_superuser)
            )
