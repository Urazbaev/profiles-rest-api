from rest_framework import permissions

# Allow user to edit their own profile
class UpdateOwnProfile(permissions.BasePermission):

    # check user is trying to edit their own profile
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
