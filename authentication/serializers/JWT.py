from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import EndPointsURLs
from core.MainVariables import NowURL
from .. import models as m
import requests

class RegisterSerializer(serializers.ModelSerializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)
  user_lang = serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields = ["first_name", "last_name", 'username', 'email', 'password', "user_lang"]
  def create(self, validated_data):
    try:
      request = self.context.get("request")
      if User.objects.filter(username=validated_data['username']).exists():
        raise Exception("This username is already taken.")
      if User.objects.filter(email=validated_data['email']).exists():
        raise Exception("This email is already registered.")
      user = User.objects.create_user(first_name=validated_data['first_name'], last_name=validated_data['last_name'], username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
      user_auth = m.Users.objects.create(user=user, preferred_language="ar" if validated_data['user_lang'] == "ar" else "en" )
      u = requests.post(f"{NowURL(request)}/{EndPointsURLs.objects.filter(id=1).first().url}", json={"username": validated_data["username"], "password": validated_data["password"]} ).json()
      u["message"] = str(u["message"]).replace("logged in", "registered")
      return u
    except Exception as e:
      return {"status": False, "error": str(e)}

class TokenObtainPairSerializer(BaseTokenSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token["full_name"] = user.get_full_name()
    token['username'] = user.username
    token['email'] = user.email
    token['is_staff'] = user.is_staff
    token['role'] = 'admin' if user.is_staff else 'user'
    return token
