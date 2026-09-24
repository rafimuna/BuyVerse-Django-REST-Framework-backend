from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


def get_or_create_cart(request):
    """
    Return the cart for the current user.
    Authenticated user: Cart is connected to request.user.
    Guest user: Cart is connected to Django session_key.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    # Guest user logic
    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    request.session.modified = True  # Cookie আপডেট নিশ্চিত করতে
    return cart


class OptionalJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except Exception:
            # টোকেন এক্সপায়ার্ড বা ইনভ্যালিড হলে Guest Mode হিসেবে কাজ করবে
            return None


class CartRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    authentication_classes = [OptionalJWTAuthentication]

    def get_object(self):
        return get_or_create_cart(self.request)


# 🟢 ফিক্সড: CreateAPIView থেকে ListCreateAPIView করা হয়েছে (GET + POST সাপোর্ট করবে)
class CartItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = [OptionalJWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        """GET /api/cart/items/ এর জন্য ইউজারের কার্ট আইটেমগুলো ফিল্টার করবে"""
        cart = get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart)

    @transaction.atomic
    def perform_create(self, serializer):
        cart = get_or_create_cart(self.request)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        # Product already exists in cart
        if cart_item:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                raise ValidationError(
                    {"quantity": f"Only {product.stock} items are available."}
                )

            cart_item.quantity = new_quantity
            cart_item.save(update_fields=["quantity"])

        # Product does not exist in cart
        else:
            if quantity > product.stock:
                raise ValidationError(
                    {"quantity": f"Only {product.stock} items are available."}
                )

            serializer.save(cart=cart)


class CartItemUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = [OptionalJWTAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ["patch"]

    def get_queryset(self):
        cart = get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart)

    @transaction.atomic
    def perform_update(self, serializer):
        product = serializer.instance.product
        quantity = serializer.validated_data.get(
            "quantity", serializer.instance.quantity
        )

        if quantity > product.stock:
            raise ValidationError(
                {"quantity": f"Only {product.stock} items are available."}
            )

        serializer.save()


class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = [OptionalJWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart = get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart)