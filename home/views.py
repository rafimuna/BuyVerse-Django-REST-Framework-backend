from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .models import Banner
from .serializers import BannerSerializer

# Product app থেকে মডেল ও সিরিয়ালাইজার ইমপোর্ট
from products.models import Product
from products.serializers import ProductSerializer


class HomePageDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # ১. Home App এর সক্রিয় ব্যানার ডাটা
        banners = Banner.objects.filter(is_active=True)
        banner_serializer = BannerSerializer(
            banners, many=True, context={'request': request}
        )

        # ২. Product App থেকে Featured ৮টি প্রোডাক্ট ডাটা (Database Query Optimized)
        featured_products = Product.objects.filter(
            is_featured=True, 
            is_active=True
        )[:8]
        
        product_serializer = ProductSerializer(
            featured_products, many=True, context={'request': request}
        )

        # ৩. একসাথে ডিকশনারি/অবজেক্ট হিসেবে রেসপন্স পাঠানো
        return Response({
            'banners': banner_serializer.data,
            'featured_products': product_serializer.data,
        }, status=status.HTTP_200_OK)


class BannerListAPIView(generics.ListCreateAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # 👈 নিশ্চিত করবে যেন Image field-এর ফুল Absolute URL (http://127.0.0.1:8000/media/...) রেসপন্সে যায়
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context