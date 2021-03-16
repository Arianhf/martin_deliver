
from .models import Courier
from .serializers import CourierSignupSerializer, CourierSerializer, CollectionSerializer, CollectionSignupSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

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