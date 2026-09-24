from django.db import transaction
from kombu.exceptions import OperationalError
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order
from .serializers import OrderSerializer
from .tasks import send_order_confirmation


class OptionalJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except Exception:
            return None


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [OptionalJWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user

        # 🟢 ২. Guest ইউজার যদি GET রিকোয়েস্ট পাঠায়, তবে খালি লিস্ট দেখাবে
        if not user.is_authenticated:
            return Order.objects.none()

        queryset = (
            Order.objects
            .select_related(
                "user",
                "shipping_method",
                "coupon",
            )
            .prefetch_related(
                "items__product"
            )
        )

        # 🟢 ৩. Staff হলে সব দেখবে, সাধারণ ইউজার হলে শুধু তার নিজের অর্ডার
        if user.is_staff:
            return queryset

        return queryset.filter(
            user=user
        )

    def perform_create(self, serializer):
        user = self.request.user
        
        # 🟢 ৪. ইউজার Authenticated হলে user ফিল্ডে অ্যাসাইন হবে,Guest হলে None থাকবে
        if user.is_authenticated:
            order = serializer.save(user=user)
        else:
            order = serializer.save(user=None)

        # Celery Task Trigger
        def enqueue_confirmation():
            try:
                send_order_confirmation.delay(order.id)
            except OperationalError:
                # Order creation must not fail when the broker is unavailable.
                pass

        transaction.on_commit(enqueue_confirmation)


class OrderRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] # 🟢 ৫. নির্দিষ্ট অর্ডার দেখার জন্য অবশ্যই Authenticated থাকা লাগবে

    def get_queryset(self):
        user = self.request.user

        queryset = (
            Order.objects
            .select_related(
                "user",
                "shipping_method",
                "coupon",
            )
            .prefetch_related(
                "items__product"
            )
        )

        if user.is_staff:
            return queryset

        return queryset.filter(
            user=user
        )