from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework")
    ),
    
    path('api/accounts/', include('accounts.urls')), 
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
    'api/categories/',
    include('categories.urls')
),

 path('api/products/', include('products.urls')),
 path('api/brands/', include('brands.urls')),
 path(
    "api/orders/",
    include("orders.urls")
),
path(
    "api/",
    include("home.urls")
),
 path(
        "api/cart/",
        include("cart.urls")
    ),
path(
    "api/shipping/",
    include("shipping.urls")
),
path(
    "api/coupons/",
    include("coupons.urls")
),
path(
    "api/wishlist/",
    include("wishlist.urls")
),
path(
    "api/payments/",
    include("payments.urls")
),
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
