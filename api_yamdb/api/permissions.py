from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_staff)


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Возможно но не сейчас)'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (
                    request.user.is_authenticated and request.user.role == 'admin')
                )
