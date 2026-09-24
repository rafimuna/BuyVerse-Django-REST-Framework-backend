from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.permissions import IsAdmin

from .models import Brand
from .serializers import BrandSerializer


class BrandListCreateAPIView(generics.ListCreateAPIView):
	serializer_class = BrandSerializer
	parser_classes = [MultiPartParser, FormParser]
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_fields = ["is_active"]
	search_fields = ["name", "slug", "description"]
	ordering_fields = ["name", "created_at", "updated_at"]
	ordering = ["name"]

	def get_permissions(self):
		if self.request.method == "GET":
			return []
		return [IsAdmin()]

	def get_queryset(self):
		queryset = Brand.objects.all()
		if self.request.method == "GET" and not (
			self.request.user.is_authenticated
			and self.request.user.role == "ADMIN"
		):
			queryset = queryset.filter(is_active=True)
		return queryset


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = BrandSerializer
	parser_classes = [MultiPartParser, FormParser]

	def get_permissions(self):
		if self.request.method in ["GET", "HEAD", "OPTIONS"]:
			return []
		return [IsAdmin()]

	def get_queryset(self):
		queryset = Brand.objects.all()
		if self.request.method == "GET" and not (
			self.request.user.is_authenticated
			and self.request.user.role == "ADMIN"
		):
			queryset = queryset.filter(is_active=True)
		return queryset
