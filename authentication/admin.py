from django.contrib import admin
from . import models as m

admin.site.site_title = "MediaDrop - Admin Panal"

admin.site.register(m.Users)
admin.site.register(m.GitHubAuth)
admin.site.register(m.GoogleAuth)
