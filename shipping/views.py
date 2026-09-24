
from rest_framework import generics
from .models import ShippingMethod , Address
from .serializers import ShippingMethodSerializer, AddressSerializer


class ShippingMethodListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShippingMethod.objects.all()
    serializer_class =ShippingMethodSerializer

class AddressListCreateAPIView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ShippingMethodRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShippingMethod.objects.all()
    serializer_class =ShippingMethodSerializer

class AddressRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

