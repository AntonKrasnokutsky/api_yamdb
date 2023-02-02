from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    'Изменение чужого контента запрещено!'
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user == obj.author
        )


class IsUserOrReadOnly(permissions.BasePermission):
    """
    'Изменение чужих подписок запрещено'
    """
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user == obj.user
        )
