from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Customer, PaymentIntent
from .serializers import CustomerSerializer, PaymentIntentSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


# TO create POST /payment_intents/ endpoint
class PaymentIntentCreateView(CreateAPIView):
    queryset = PaymentIntent.objects.all()
    serializer_class = PaymentIntentSerializer
    permission_classes = [AllowAny]


# To create GET  /payment_intents/<id>/
class PaymentIntentDetailView(RetrieveAPIView):
    queryset = PaymentIntent.objects.all()
    serializer_class = PaymentIntentSerializer
    permission_classes = [AllowAny]
