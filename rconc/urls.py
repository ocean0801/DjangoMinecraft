from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('query', views.query),
    path('script/<int:ids>/', views.script, name='script'),
    path('script/', views.scriptindex, name='script'),
    path('profile/<int:ids>/', views.profile, name='script'),
    path('profile/', views.profileindex, name='script'),
    path('code/<int:ids>/', views.code, name='script'),
    path('code/', views.codeindex, name='script'),
    path('console/',views.console,name='submit'),
    path('config/',views.config_page,name='submit2'),
    path('help/',views.help,name='help'),
]