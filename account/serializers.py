from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from .models import OTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # exclude password, groups, permission, is_superuser
        exclude = ['password', 'is_superuser', 'is_staff', 'groups', 'user_permissions']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ActivateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField(max_length=6)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        return data

# class PasswordChangeSerializer(serializers.Serializer):
#     pass
#     # Add fields for password change (e.g., old_password, new_password)
#     # Example:
#     # old_password = serializers.CharField()
#     # new_password = serializers.CharField()

# class PasswordResetSerializer(serializers.Serializer):
#     pass
#     # Add fields for password reset (e.g., email)
#     # Example:
#     # email = serializers.EmailField()

# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = ['user', 'otp', 'created']

#     def validate(self, data):
#         # Validate OTP expiration
#         if data['created'] + timezone.timedelta(minutes=20) < timezone.now():
#             raise serializers.ValidationError("OTP has expired.")
#         return data
