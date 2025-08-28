from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.urls import path, include
from django.http import JsonResponse
from django.contrib import admin
from django.conf import settings
from . import handlers as h

urlpatterns = [
  path('admin/', admin.site.urls),
  path('status/', h.status),
  
  ## APIs ##
  path('api/auth/', include('authentication.urls')),
  #path('api/site/', include('site_api.urls')),
  
]
                
if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'shopsphere.handlers.error404'
handler500 = 'shopsphere.handlers.error500'
