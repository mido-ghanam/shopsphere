from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django.urls import path
from . import views as v

urlpatterns = [
  ## JWT Authentication URLs ##
  path('register/', v.JWT.RegisterView.as_view(), name='register_api'),
  path('login/', v.JWT.LoginView.as_view(), name='login_api'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify_api'),
  path('logout/', v.JWT.LogoutView.as_view(), name='logout_api'),
  path("oauth/<str:oauth_provider>/", v.oauth.oauth_redirect, name="oauth_redirect"),
  path("oauth/<str:oauth_provider>/callback/", v.oauth.oauth_callback, name="oauth_callback"),
  
]
