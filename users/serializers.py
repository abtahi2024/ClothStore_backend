from users.models import User

import requests
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer


class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        token = attrs.get("access_token")

        # Google userinfo endpoint
        google_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(
            google_url,
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code != 200:
            raise serializers.ValidationError("Invalid Google token")

        data = response.json()

        email = data.get("email")
        if not email:
            raise serializers.ValidationError("Google account has no email")

        # User create or get
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": data.get("given_name", ""),
                "last_name": data.get("family_name", ""),
            }
        )

        # JWT token generate
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "address",
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        return user

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model=User
        fields=['id','email','password','first_name','last_name','address','phone_number']


class UserSerializer(BaseUserSerializer):
    image=serializers.ImageField(required=False)
    class Meta(BaseUserSerializer.Meta):
        model=User
        ref_name='CustomUser'
        fields=['id','image','email','first_name','last_name','address','phone_number','is_staff']
        read_only_fields=['is_staff']
        
        extra_kwargs = {
            "image": {"required": False}
        }