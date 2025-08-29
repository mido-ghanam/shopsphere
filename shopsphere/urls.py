from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from . import handlers as h, views as v
from django.urls import path, include
from django.http import JsonResponse
from django.contrib import admin
from django.conf import settings

urlpatterns = [
  path('admin/', admin.site.urls),
  path('status/', h.status),
  
  ## JWT Authentication URLs ##
  path('api/auth/login/', v.JWT.LoginView.as_view(), name='login_api'),
  path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
  path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify_api'),
  path('api/auth/logout/', v.JWT.LogoutView.as_view(), name='logout_api'),
  
]
                
if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'shopsphere.handlers.error404'
handler500 = 'shopsphere.handlers.error500'
