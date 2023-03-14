from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # override has_object_permission method
    def has_object_permission(self, request, view, obj):
        # check if user is requesting read only access and return True
        if request.method in permissions.SAFE_METHODS:
            return True
        # return True only if the user owns the profile
        return obj.owner == request.user
