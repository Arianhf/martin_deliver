from rest_framework.permissions import BasePermission
from .models import Collection, Package

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

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Package):
            try:
                collection = Collection.objects.get(email=request.user.email)
            except:
                collection = None
        
            return obj.sender == collection
        else:
            return True