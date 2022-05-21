from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    def has_object_permission(self, request, view, obj):
        return bool(obj.user is request.user or request.user.is_staff)
