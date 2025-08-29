from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .. import models as m

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
