import uuid

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order

from .models import Payment


class PaymentProcessAPIView(APIView):
	permission_classes = [AllowAny]

	@transaction.atomic
	def post(self, request):
		order_id = request.data.get("order_id")
		payment_method = request.data.get("payment_method")

		if not order_id or not payment_method:
			return Response(
				{"detail": "order_id and payment_method are required."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if payment_method not in dict(Payment.PAYMENT_METHOD_CHOICES):
			return Response(
				{"detail": "Invalid payment method."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		try:
			order = Order.objects.select_for_update().get(pk=order_id)
		except (Order.DoesNotExist, ValueError):
			return Response(
				{"detail": "Order not found."},
				status=status.HTTP_404_NOT_FOUND,
			)

		user = request.user
		if user.is_authenticated and order.user_id != user.id and not user.is_staff:
			return Response(
				{"detail": "You do not have permission to pay for this order."},
				status=status.HTTP_403_FORBIDDEN,
			)

		payment, created = Payment.objects.get_or_create(
			order=order,
			defaults={
				"payment_method": payment_method,
				"amount": order.total,
				"transaction_id": f"SIM-{uuid.uuid4().hex[:12].upper()}",
				"status": "successful",
				"paid_at": timezone.now(),
			},
		)

		if created:
			order.payment_status = "paid"
			order.save(update_fields=["payment_status", "updated_at"])

		return Response(
			{
				"message": "Payment processed successfully (simulation).",
				"payment_id": payment.id,
				"order_id": order.id,
				"amount": payment.amount,
				"payment_method": payment.payment_method,
				"transaction_id": payment.transaction_id,
				"status": payment.status,
			},
			status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
		)

# Create your views here.
