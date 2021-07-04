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

class IsSystemBackEndUser(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):

        # if request.method in permissions.SAFE_METHODS:
        #     return False
        # else:
        if not request.user.is_anonymous:
            if request.user.staff or request.user.admin:
                return True
            else:
                return False

class IsAnonymousUser(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):

        # if request.method in permissions.SAFE_METHODS:
        #     return False
        # else:
        if request.user.is_anonymous or request.user.admin:
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


