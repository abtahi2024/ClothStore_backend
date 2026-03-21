from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
import requests
from rest_framework import status
from users.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import *

#  POST http://127.0.0.1:8000/auth/google/login/
# {
#   "access_token": "GOOGLE_ACCESS_TOKEN_HERE"
# }
class GoogleLoginSuccess(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "access": serializer.validated_data["access"],
            "refresh": serializer.validated_data["refresh"],
            "email": serializer.validated_data["user"].email,
        })

# {
#   "email": "test@gmail.com",
#   "password": "12345678",
#   "first_name": "Test",
#   "last_name": "User",
#   "phone_number": "01700000000",
#   "address": "Dhaka"
# }
class RegisterView(APIView):
    """only for register"""
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        
        
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {
#   "refresh": "REFRESH_TOKEN"
# }
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                "access": str(refresh.access_token)
            })
        except TokenError:
            return Response(
                {"error": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )