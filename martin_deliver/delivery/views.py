from .models import Courier, Collection, Package
from .serializers import (
    CourierSignupSerializer,
    CourierSerializer,
    CollectionSerializer,
    CollectionSignupSerializer,
    PackageCreateSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework import status, permissions, mixins, generics
from .permissions import IsCollection

from rest_framework_simplejwt.views import TokenObtainPairView

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CourierCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSignupSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CourierList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CollectionCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Courier.objects.all()
    serializer_class = CollectionSignupSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CollectionList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class PackageCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageCreateSerializer
    permission_classes = [IsCollection]

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.user = request.user
        return self.create(request, *args, **kwargs)

    