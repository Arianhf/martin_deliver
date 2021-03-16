from rest_framework.permissions import BasePermission
from .models import Collection

class IsCollection(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        try:
            collection = Collection.objects.get(email=request.user.email)
        except:
            collection = None
        return bool(
            request.user and
            request.user.is_authenticated and
            collection
        )