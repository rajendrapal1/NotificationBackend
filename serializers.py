from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer
)

from .models import UserProfile

from notifications.models import Trigger
from notifications.services.notification import send_notification


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    phone_number = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "password",
            "confirm_password"
        ]

    def validate(self, data):

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "Passwords do not match."
            )

        return data

    def create(self, validated_data):

        phone_number = validated_data.pop("phone_number")

        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number
        )

        print("User created:", user.username)

        # Registration notification
        try:
            result = send_notification(
                user=user,
                subject="Registration Successful",
                message=(
                    f"Hi {user.username}, "
                    "your registration was successful."
                )
            )

            print("Registration notification:", result)

        except Exception as e:
            print(
                "Registration notification error:",
                e
            )

        return user


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        # JWT authentication
        data = super().validate(attrs)

        user = self.user

        print("Django Login Successful:", user.username)

        try:
            trigger = Trigger.objects.get( name="Login",is_active=True)

            print("FOUND LOGIN TRIGGER:", trigger)
    
            # send_notification method
            result = send_notification(user=user,subject="Login Successful",message=(f"Hi {user.username},""you have successfully logged in."))

            print("Login Trigger Result:", result)

        except Trigger.DoesNotExist:
            print("Login trigger not found.")

        except Exception as e:
            print("Login notification error:", e)

        return data
