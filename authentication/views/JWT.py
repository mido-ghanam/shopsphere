from rest_framework_simplejwt.views import TokenRefreshView as SimpleTokenRefreshView
from ..serializers import RegisterSerializer, TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from .. import models as m
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    serializer = RegisterSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
      try:
        result = serializer.save()
        return Response(result, status=201)
      except Exception as e:
        return Response({"status": False, "error": str(e)}, status=500)
    return Response({"status": False, "error": serializer.errors}, status=400)

class LoginView(TokenObtainPairView):
  serializer_class = TokenObtainPairSerializer
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    tokens = response.data
    user = User.objects.filter(username=request.data.get("username")).first()
    custom_response = {
      "status": True,
      "message": "User logged in successfully",
      "tokens": {
        "access": tokens.get("access"),
        "refresh": tokens.get("refresh")
      },
    }
    return Response(custom_response, status=response.status_code)

class LogoutView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    try:
      refresh_token = request.data.get("refresh")
      if not refresh_token:
        return Response({"error": "refresh token is required"}, status=400)
      token = RefreshToken(refresh_token)
      token.blacklist()
      return Response({"message": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
      return Response({"error": str(e)}, status=400)
