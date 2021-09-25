from rest_framework import serializers
from .models.store_manager_models import store_detail,CustomerData


class StoreSerializer(serializers.Serializer):
    storeID = serializers.CharField(max_length=150)
    store_name = serializers.CharField(max_length=80)
    store_location = serializers.CharField(max_length=30)
    store_town = serializers.CharField(max_length=30)
    store_city = serializers.CharField(max_length=30)
    store_state = serializers.CharField(max_length=30)
    store_category = serializers.CharField(max_length=100)
    store_subcategory = serializers.CharField(max_length=100)
    statusflag = serializers.BooleanField(default=1)
    time_stamp = serializers.DateTimeField()


class CustomerDataSerializer(serializers.Serializer):
    storeID = serializers.CharField(max_length=150) 
    name = serializers.CharField(max_length=150,default='NA')
    contact = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=100,default='NA')
    DOB = serializers.CharField(max_length=10, default='NA')
    gender = serializers.CharField(max_length=6,default='NA')
    DOM = serializers.CharField(max_length=10,default='NA')
    entry_type = serializers.CharField(max_length=10)
    time_stamp = serializers.DateTimeField()