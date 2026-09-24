from rest_framework import serializers
from .models import ShippingMethod , Address

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [ 'name', 'cost', 'estimated_days']


class  AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Address
        fields = ['user', 'full_name', 'phone',  'city', 'postal_code', 'country']