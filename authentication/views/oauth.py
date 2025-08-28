from core.utils import exchange_code_google, exchange_code_github, getUserTokens
from core.MainVariables import GoogleOAuth, GitHubOAuth, BaseURLs, WebSiteURL
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from urllib.parse import urlencode
import base64, json, requests
from .. import models as m

def oauth_redirect(request, oauth_provider=None):
  gg = request.GET
  oauth_provider, redirect_to, operator = oauth_provider.lower() if oauth_provider else None, gg.get("red", ""), gg.get("operator", "")
  if oauth_provider not in ["google", "github"]:
    return JsonResponse({"status": False, "error": f"OAuth Provider: '{oauth_provider}' isn't supported"}, status=403)
  if operator not in ["login", "register"]:
    return JsonResponse({"status": False, "error": f"Operator: '{operator}' not supported..."}, status=403)
  if oauth_provider == "google":
    url = f"{BaseURLs['GoogleOAuth']['auth']}?{urlencode({k: v for k, v in GoogleOAuth.items() if k not in ['client_secret']})}"
  if oauth_provider == "github":
    url = f"{BaseURLs['GitHubOAuth']['auth']}?{urlencode({k: v for k, v in GitHubOAuth.items() if k not in ['client_secret']})}"
  url += "&state=" + base64.urlsafe_b64encode(json.dumps({"red": redirect_to}).encode()).decode() + f"-{operator}"
  return JsonResponse({"status": True, f"{oauth_provider}_url": url})

def oauth_callback(request, oauth_provider=None):
  gg = request.GET
  oauth_provider, state_raw, code = oauth_provider.lower() if oauth_provider else None, gg.get("state"), gg.get("code")
  if oauth_provider not in ["google", "github"]: return JsonResponse({"status": False, "error": f"OAuth Provider: '{oauth_provider}' not supported"}, status=403)
  if not state_raw or not code: return JsonResponse({"status": False, "error": "Missing state or code"}, status=400)
  state_raw, operator = state_raw.split("-")
  state_data = json.loads(base64.urlsafe_b64decode(state_raw.encode()).decode())
  red_url = state_data.get("red", WebSiteURL)
  if oauth_provider == "google":
    res = exchange_code_google(code)
    sub, email = res.get("id_token", {}).get("payload", {}).get("sub"), res.get("id_token", {}).get("payload", {}).get("email")
    userOAuth = m.GoogleAuth.objects.filter(sub=sub)
    if userOAuth.exists():
      user = userOAuth.first().user.user
      res = {"status": True, "message": "Login successful", "tokens": getUserTokens(user), "redirect_to": red_url}
      if not m.Users.objects.get(user=user).is_activate:
        res["action"] = "activate_account"
      return JsonResponse(res, status=200)
    if operator == "login": return JsonResponse({"status": False, "error": "Your Google Account wasn't linked to an account yet. Please register first."}, status=401)
    elif operator == "register":
      user_data = res.get("id_token", {}).get("payload", {})
      if User.objects.filter(username=email.split("@")[0]).exists(): return JsonResponse({"status": False, "error": "Username already exists. Please choose a different username."}, status=409)
      if User.objects.filter(email=user_data.get("email")).exists(): return JsonResponse({"status": False, "error": "Google Account already exists by another auth method. Please login."}, status=409)
      user = User.objects.create_user(first_name=user_data.get("given_name"), last_name=user_data.get("family_name"), username=user_data.get("email").split("@")[0], email=user_data.get("email"))
      user.set_unusable_password(), user.save()
      user_ac = m.Users.objects.create(user=user, actived_account=True)
      m.GoogleAuth.objects.create(user=user_ac, sub=sub)
      return JsonResponse({"status": True, "message": "Registration successful", "tokens": getUserTokens(user), "redirect_to": red_url}, status=200)
  elif oauth_provider == "github":
    res = exchange_code_github(code)
    if res.get("error"): return JsonResponse({"status": False, "error": str(res)}, status=400)
    userOAuth = m.GitHubAuth.objects.filter(user_github_id=res.get("id"))
    if userOAuth.exists():
      user = userOAuth.first().user.user
      return JsonResponse({"status": True, "message": "Login successful", "tokens": getUserTokens(user), "redirect_to": red_url}, status=200)
    if operator == "login": return JsonResponse({"status": False, "error": "Your GitHub Account wasn't linked to an account yet. Please register first."}, status=401)
    elif operator == "register":
      user_data, email = res, res.get("email")
      if User.objects.filter(username=user_data.get("login")).exists(): return JsonResponse({"status": False, "error": "GitHub Account already exists. Please login."}, status=409)
      if email and User.objects.filter(email=email).exists(): return JsonResponse({"status": False, "error": "Email already exists. Please use a different email."}, status=409)
      user = User.objects.create_user(first_name=user_data.get("name", "").split(" ")[0], last_name=user_data.get("name", "").split(" ")[1] if " " in user_data.get("name", "") else "", username=user_data.get("login"), email=email)
      user.set_unusable_password(), user.save()
      user_ac = m.Users.objects.create(user=user, actived_account=False)
      m.GitHubAuth.objects.create(user=user_ac, user_github_id=user_data.get("id"), avatar_url=user_data.get("avatar_url"))
      return JsonResponse({"status": True, "message": "Your GitHub account has been linked successfully.", "tokens": getUserTokens(user), "redirect_to": red_url}, status=200)
  return JsonResponse({"status": False, "error": "Unhandled case"}, status=400)
