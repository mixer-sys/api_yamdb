from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_staff)


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (
                    request.user.is_authenticated
                    and request.user.role == 'admin')
                )


class IsAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.role in ('moderator', 'admin'))

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in ('moderator', 'admin'):
                return True
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
