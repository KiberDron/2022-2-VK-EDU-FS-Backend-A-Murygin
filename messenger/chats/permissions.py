from rest_framework import permissions
from .models import ChatMember


class IsMemberOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return ChatMember.objects.filter(chat_id=obj.id, user_id=request.user.id).exists()
        return ChatMember.objects.filter(chat_id=obj.id, user_id=request.user.id, is_admin=True).exists()


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return ChatMember.objects.filter(chat_id=view.kwargs['chat_id'], user_id=request.user.id).exists()


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author_id == request.user.id


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return ChatMember.objects.filter(chat_id=view.kwargs['pk'], user_id=request.user.id, is_admin=True).exists()
