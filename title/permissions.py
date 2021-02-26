from rest_framework import permissions

from auth_user.models import Roles


class IsYAMDBPermission(permissions.BasePermission):
    """Права для проекта YAMDB."""

    def has_object_permission(self, request, view, obj):
        return bool((request.method in permissions.SAFE_METHODS)
                    or (obj.author == request.user)
                    or (request.user.role in (Roles.ADMIN, Roles.MODERATOR, )))


class IsStaffOrReadOnly(permissions.BasePermission):
    """Права для admin или any."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_staff and request.user.is_superuser)
