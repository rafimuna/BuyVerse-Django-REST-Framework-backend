from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import  ExampleView, AdminDashboardview, RegisterListCreateAPIView,RegisterRetrieveUpdateDestroyAPIView , LogoutAPIView, UserProfileView  # Import your view class
from .serializers import CustomTokenObtainPairSerializer

# Custom View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    # This maps the view to the /students/ endpoint
    path('example/',  ExampleView.as_view(), name="example"),
    path('admin/',  AdminDashboardview.as_view(), name="admin"),
    path('register/',  RegisterListCreateAPIView.as_view(), name="admin"),
    path('register/update',  RegisterRetrieveUpdateDestroyAPIView.as_view(), name="admin"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout"
    ),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]