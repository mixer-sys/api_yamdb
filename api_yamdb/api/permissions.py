from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Изменить контент может только админ.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_staff))


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_staff)
