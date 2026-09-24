from django.urls import path

from .views import PaymentProcessAPIView


urlpatterns = [
    path("process/", PaymentProcessAPIView.as_view(), name="payment-process"),
]