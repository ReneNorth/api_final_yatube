# from rest_framework.permissions import (BasePermission,
#                                         SAFE_METHODS,
#                                         IsAuthenticated)
# from django.contrib.admin import is_auth
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class PostsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class CommentsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)

