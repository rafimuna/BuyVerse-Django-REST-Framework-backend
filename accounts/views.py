from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterSerializer, LogoutSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from accounts.permissions import IsAdmin


User = get_user_model()

class RegisterListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class RegisterRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)






class ExampleView(APIView):
    authentication_classes = [
        JWTAuthentication
    ]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "user": request.user.username,
            "message": "Authenticated successfully"
        })

class AdminDashboardview(APIView) :

    authentication_classes = [
        JWTAuthentication
        
    ]

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        return Response({
            "user": request.user.username,
            "message": "Welcome to admindashboard"
        })

class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Successfully logged out."
            },
            status=status.HTTP_205_RESET_CONTENT
        )
