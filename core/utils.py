import base64, requests, time, random
from email.mime.text import MIMEText
from .MainVariables import HostURL
from user_agents import parse
from . import jwt_extract

url = HostURL

def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip

def get_user_agent(request):
  user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
  if user_agent.is_mobile:
    device_type = "Mobile"
  elif user_agent.is_pc:
    device_type = "Computer"
  else:
    device_type = "Unknown Device"
  os = user_agent.os.family
  browser = user_agent.browser.family
  return {'device_type': device_type, 'os': os, 'browser': browser,}


def getUserTokens(user):
  refresh = RefreshToken.for_user(user)
  return {"refresh": str(refresh), "access": str(refresh.access_token)}
