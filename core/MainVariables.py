from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlparse

HostURL = "https://apis.mediadrop.midoghanam.site"
WebSiteURL = "https://mediadrop.midoghanam.site"
CodeSpaceURL = "https://shiny-computing-machine-rjg65v5p4xxhp9q9-8000.app.github.dev"

def NowURL(request):
  return request.scheme + "://" + request.get_host()

def get_page_url(request):
  referer = request.META.get('HTTP_REFERER', '')
  return urlparse(referer).path if referer else '/'

GoogleOAuth = {
  'client_id': "15653912530-ti0c8p8ncq7v4va8pi6gikp12jui5k5g.apps.googleusercontent.com",
  'redirect_uri': f'{HostURL}/auth/oauth/google/callback/',
  'scope': 'openid email profile',
  'response_type': 'code',
  'access_type': 'offline',
  'prompt': 'consent',
  "client_secret": "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"
}

#params = {k: v for k, v in GoogleOAuth.items() if k != 'prompt'}

GitHubOAuth = {
  'client_id': 'Ov23liT1BHS8kRp2WmgF',
  'redirect_uri': f'{HostURL}/auth/oauth/github/callback/',
  'scope': 'read:user',
  'allow_signup': 'true',
  'client_secret': "21e3189641f57af0bef8f1fd4ac484cc6bd9e6f1",
}

BaseURLs = {
  "GoogleOAuth": {
    "auth": "https://accounts.google.com/o/oauth2/v2/auth",
    "getTokens": "https://oauth2.googleapis.com/token",
    "emailAPI": {
      "send": "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
    },
    "user": {
      "info": "https://www.googleapis.com/oauth2/v3/userinfo",
    },

  },
  "GitHubOAuth": {
    "auth": "https://github.com/login/oauth/authorize",
    "getTokens": "https://github.com/login/oauth/access_token",
    'users': "https://api.github.com/user",
    "emails": "https://api.github.com/user/emails",
  },
}

MainVars = {
  "mediadrop": {
    "gmail": {
      "refresh_token": "1//03yWBFcCZlAYPCgYIARAAGAMSNwF-L9IrXpWFEMDe4ahJh5Eo4n9wMNUjndjVFpUhPE60ex_9adLF_fLF8rUj4eJIc6qjnIISw_o",
    }
  }
}

_mediadrop_access_token = {
  "token": None,
  "expires_at": 0
}
