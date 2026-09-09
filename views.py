from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

from .serializers import (
    RegisterSerializer,
    LoginSerializer
)


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer( data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User registered successfully."
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer( data=request.data)

        if serializer.is_valid():

            return Response(
                {
                    "message": "Login successful.",
                    "access": serializer.validated_data["access"],
                    "refresh": serializer.validated_data["refresh"]
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )