import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from photo_conversion.models import PhotoConversion
from .utils import generate_otp, save_otp, verify_otp
from .serializers import UserDetailSerializer, RegisterSerializer, ActivateUserSerializer, LoginSerializer
# PasswordChangeSerializer, PasswordResetSerializer
from photo_conversion.serializers import PhotoConversionDetailSerializer
from .utils import send_mail
from core.response import MyResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from constants import currently_hosted_domain
from django.shortcuts import render


class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            otp = save_otp(user)
            print(otp)
            mail_data = {
                "template": "email/otp_email.html",
                "subject": "Welcome to Color Memoir!",
                "to": [user.email],
                "username": user.username,
                "otp": otp,
                "alt_link": currently_hosted_domain + reverse("activate", kwargs={"username": user.username, "otp": otp}),
            }
            send_mail(mail_data)
            return MyResponse.success(data=serializer.data, message='User registered successfully. Check your email for OTP.', status_code=status.HTTP_201_CREATED)
        return MyResponse.failure(data=serializer.errors, message='User registration failed.', status_code=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    def get(self, request, username, otp, format=None):
        serializer = ActivateUserSerializer(data={
            'username': username,
            'otp': otp
        })
        if serializer.is_valid():
            username = serializer.data['username']
            otp_input = serializer.data['otp']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return MyResponse.failure(message='User not found.', status_code=status.HTTP_404_NOT_FOUND)

            if verify_otp(user, otp_input):
                user.is_active = True
                user.save()
                return MyResponse.success(data=serializer.data, message='User activated successfully.', status_code=status.HTTP_200_OK)
            else:
                return MyResponse.failure(message='Invalid OTP.', status_code=status.HTTP_400_BAD_REQUEST)

        return MyResponse.failure(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return MyResponse.success(data={'token': token.key}, status_code=status.HTTP_200_OK)
            else:
                return MyResponse.failure(message='Invalid credentials.', data=request.data, status_code=status.HTTP_401_UNAUTHORIZED)

        return MyResponse.failure(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # logout and also delete the token
        token = request.auth
        token.delete()
        logout(request)
        return MyResponse.success(message='Logout successful.', status_code=status.HTTP_200_OK)


class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer_user = UserDetailSerializer(user)
        conversions = PhotoConversion.objects.filter(user=user)
        serializer_conversions = PhotoConversionDetailSerializer(
            conversions, many=True)
        return MyResponse.success(data={'user': serializer_user.data, 'conversions': serializer_conversions.data}, message='User profile retrieved successfully.', status_code=status.HTTP_200_OK)


class CheckEmailTemplateView(APIView):
    def get(self, request, format=None):
        return render(request, 'email/otp_email.html', {
            "username": "darpan.kattel",
            "otp": "123456",
            "alt_link": currently_hosted_domain + reverse("activate", kwargs={"username": "darpan.kattel", "otp": "123456"}),
        })

# class PasswordChangeView(APIView):
#     def post(self, request, format=None):
#         serializer = PasswordChangeSerializer(data=request.data)
#         if serializer.is_valid():
#             # Implement password change logic here
#             return MyResponse.success({'detail': 'Password changed successfully.'}, status_code=status.HTTP_200_OK)

#         return MyResponse.success(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

# class PasswordResetView(APIView):
#     def post(self, request, format=None):
#         serializer = PasswordResetSerializer(data=request.data)
#         if serializer.is_valid():
#             # Implement password reset logic here
#             return MyResponse.success({'detail': 'Password reset email sent successfully.'}, status_code=status.HTTP_200_OK)

#         return MyResponse.success(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
