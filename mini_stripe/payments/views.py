import time
import random
import requests
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Customer, PaymentIntent, WebhookEventLog
from .serializers import CustomerSerializer, PaymentIntentSerializer


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


# Creating PaymentIntent Confirmation API
class PaymentIntentConfirmView(APIView):
    def post(self, request, pk):
        # 1: Fetch Payment Intent
        payment_intent = get_object_or_404(PaymentIntent, pk=pk)

        # 2: Prevent Double Confirmation
        if payment_intent.status in ["succeeded", "failed"]:
            return Response(
                {"error": "Payment Already Finalized"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3: Mark as processing
        payment_intent.status = PaymentIntent.StatusChoices.PROCESSING
        payment_intent.save()

        # 4: Simulate bank delay
        time.sleep(2)

        # 5: Random success/failure
        if random.random() < 0.8:
            payment_intent.status = PaymentIntent.StatusChoices.SUCCEEDED
            event_name = "payment_intent.succeeded"
        else:
            payment_intent.status = PaymentIntent.StatusChoices.FAILED
            event_name = "payment_intent.failed"

        payment_intent.save()

        # 6: Emitting Webhook Event
        event_name = (
            "payment_intent.succeeded"
            if payment_intent.status == PaymentIntent.StatusChoices.SUCCEEDED
            else "payment_intent.failed"
        )

        requests.post(
            "http://127.0.0.1:8000/webhooks/payment/",
            json={
                "event": event_name,
                "payment_intent_id": str(payment_intent.id),
                "amount": str(payment_intent.amount),
                "currency": payment_intent.currency,
            },
        )
        # 7: Respond to Client
        return Response(
            {"id": payment_intent.id, "status": payment_intent.status},
            status=status.HTTP_200_OK,
        )


class PaymentWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        event_name = request.data.get("event")
        payment_intent_id = request.data.get("payment_intent_id")
        payload = request.data

        payment_intent = get_object_or_404(PaymentIntent, id=payment_intent_id)

        WebhookEventLog.objects.create(
            event_name=event_name,
            payment_intent=payment_intent,
            payload=payload,
        )

        return Response({"status": "received"}, status=200)
