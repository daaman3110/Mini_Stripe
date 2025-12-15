from rest_framework import serializers
from .models import Customer, PaymentIntent


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


# PaymentIntent Serializer
class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = "__all__"
        read_only_fields = ["id", "status", "created_at", "updated_at"]
