from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet,
    PaymentIntentCreateView,
    PaymentIntentDetailView,
    PaymentIntentConfirmView,
    PaymentWebhookView
)
from django.urls import path

router = DefaultRouter()
router.register("customers", CustomerViewSet)

urlpatterns = [
    # PaymentIntent APIs (manual, controlled)
    path("payment_intents/", PaymentIntentCreateView.as_view()),
    path("payment_intents/<uuid:pk>/", PaymentIntentDetailView.as_view()),
    path("payment_intents/<uuid:pk>/confirm/", PaymentIntentConfirmView.as_view()),
    path("webhooks/payment/", PaymentWebhookView.as_view())
]

# Add router URLs After
urlpatterns += router.urls
