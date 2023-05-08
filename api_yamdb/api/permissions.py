from rest_framework import permissions


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """
    Доступ для автора, админа, модератора
    или любого пользователю только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdminSuperuserOrReadOnly(permissions.BasePermission):
    """
    Доступ для админа или любому пользователю только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAuthOrAdmin(permissions.BasePermission):
    """Доступ для админа или супер-юзера."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff
        )
