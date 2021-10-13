from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('query/', views.query),
    path('script/<int:ids>/', views.script, name='scripts'),
    path('script/', views.scriptindex, name='script'),
    path('script/<int:id>/<str:type>', views.script_do, name='scriptss'),
    path('script/edit/<int:id>', views.script_edit, name='submit4'),
    path('script_c/', views.script_page,name='submit3'),
    path('profile/', views.profileac, name='script'), 
    path('console/',views.console,name='submit'),
    path('config/',views.config_page,name='submit2'),
    path('help/',views.help,name='help'),
    path('test/',views.test),
    path('',views.index),
]