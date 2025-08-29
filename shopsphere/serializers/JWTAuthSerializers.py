from rest_framework import serializers
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenBackendError, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseSerializer
from ..models import Users

class TokenObtainPairSerializer(BaseSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)
    user = self.user
    try:
      user_info = Users.objects.get(user=user)
    except Users.DoesNotExist:
      user_info = None
    return {
      "tokens": {"access": data.get("access"), "refresh": data.get("refresh"),},
      "user": {
        "username": user.username,
      }
    }

class TokenVerifySerializer(serializers.Serializer):
  token = serializers.CharField()
  def _error(self, message, error=None, token_type="unknown", exp=None):
    return serializers.ValidationError({"status": False, "message": message, "error": str(error) if error else None, "token_type": token_type, "expires_at": exp, })
  def validate(self, attrs):
    token_str = attrs["token"]
    try:
      token = UntypedToken(token_str)
      payload = token.payload
      jti = payload.get("jti")
      token_type = payload.get("token_type", "unknown")
      exp_timestamp = payload.get("exp")
      exp_datetime = datetime.fromtimestamp(exp_timestamp)
      try:
        outstanding = OutstandingToken.objects.get(jti=jti)
        if BlacklistedToken.objects.filter(token=outstanding).exists():
          raise self._error("Token is blacklisted", token_type=token_type, exp=exp_datetime)
      except OutstandingToken.DoesNotExist:
        pass
      return {"status": True, "message": "Token is valid", "token_type": token_type, "expires_at": exp_datetime}
    except (InvalidToken, TokenBackendError, TokenError) as e:
      raise self._error("Invalid or expired token", error=e)
    except Exception as e:
      raise self._error("Unexpected error while verifying token", error=e)

class TokenBlacklistSerializer(serializers.Serializer):
  refresh = serializers.CharField()
  def validate(self, attrs):
    self.token = attrs["refresh"]
    return attrs
  def save(self, **kwargs):
    try:
      token = RefreshToken(self.token)
      if token["token_type"] != "refresh":
        raise serializers.ValidationError({ "status": False, "message": "Only refresh tokens can be blacklisted." })
      token.blacklist()
      return {"status": True, "message": "Token blacklisted successfully", "jti": token["jti"], "expires_at": datetime.fromtimestamp(token["exp"])}
    except TokenError as e:
      raise serializers.ValidationError({"status": False, "message": "Failed to blacklist token", "error": str(e) })
    except Exception as e:
      raise serializers.ValidationError({"status": False, "message": "Unexpected error while blacklisting token", "error": str(e)})
