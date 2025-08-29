from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django.urls import path
from . import views as v

urlpatterns = [
  ## JWT Authentication URLs ##
  path('login/', v.JWT.LoginView.as_view(), name='login_api'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify_api'),
  path('logout/', v.JWT.LogoutView.as_view(), name='logout_api'),
  
]
