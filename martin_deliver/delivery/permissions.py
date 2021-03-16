from rest_framework.permissions import BasePermission
from .models import Collection, Package, Courier

class IsCollection(BasePermission):
    """
    The request is authenticated as a user, and is a collection.
    """

    def has_permission(self, request, view):
        try:
            collection = Collection.objects.get(email=request.user.email)
        except:
            collection = None
        return bool(
            request.user and
            collection
        )

class IsCourier(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        try:
            courier = Courier.objects.get(email=request.user.email)
        except:
            courier = None
        return bool(
            request.user and
            courier
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