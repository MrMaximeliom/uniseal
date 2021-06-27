from rest_framework import permissions
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if not request.user.is_anonymous:
                if request.user.admin:
                    return True
                else:
                    return False

class UnisealPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if not request.user.is_anonymous:
                if request.user.admin:
                    return True
            else:
                return False


