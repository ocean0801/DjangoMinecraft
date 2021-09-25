from django.contrib import admin
from django.urls import include, path
import rconc.views
urlpatterns = [
    path('mine/', include('rconc.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',rconc.views.profileac)
]
