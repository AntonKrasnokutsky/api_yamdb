from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsUserOrReadOnly(permissions.BasePermission):
    """
    может публиковать отзывы и ставить оценку произведениям
    (фильмам/книгам/песенкам), может комментировать чужие отзывы;
    может редактировать и удалять свои отзывы и комментарии.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.role == 'user'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Права аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.role == 'moderator'


class IsAdministratorOrReadOnly(permissions.BasePermission):
    """
    полные права на управление всем контентом проекта.
    """
    def has_permission(self, request, view, ):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.role == 'admin'
        else:
            return False


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    полные права на управление всем контентом проекта.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.is_superuser


