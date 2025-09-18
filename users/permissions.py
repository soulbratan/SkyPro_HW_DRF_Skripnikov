from rest_framework import permissions

class IsModer(permissions.BasePermission):
    """Пользовательский пермишин для проверки нахождения в группе модераторы."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Пользовательский пермишин для проверки владельца."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

