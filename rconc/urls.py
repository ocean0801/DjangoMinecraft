from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #path('stop', views.stop),
    #path('', views.index, name='index'),
    #path('kill/<str:type>', views.kill, name='func:kill'),
    #path('give/<str:type>/<str:item>', views.give, name='func:give'),
    #path('give/<str:type>/<str:item>/<str:i>', views.give2, name='func:give2'),
    #path('effect/<str:com>/<str:type>', views.effect, name='func:effect'),
    #path('effect/<str:com>/<str:type>/<str:ef>', views.effect2, name='func:effect2'),
    #path('effect/<str:com>/<str:type>/<str:ef>/<str:time>/<str:power>', views.effect3, name='func:effect3'),
    path('query', views.query),
    path('com/<str:type>', views.test2),
    path('com/<str:type>/<str:type2>', views.test3),
    path('com/<str:type>/<str:type2>/<str:type3>', views.test4),
    path('com/<str:type>/<str:type2>/<str:type3>/<str:type4>', views.test5),
    #path('test/<str:com>/<str:type>', views.test, name='func:effect'),
    path('line/', views.hennkann, name='cline'),
    path('script/<int:ids>/', views.script, name='script'),
    path('script/', views.scriptindex, name='script'),
    path('profile/<int:ids>/', views.profile, name='script'),
    path('profile/', views.profileindex, name='script'),
    path('code/<int:ids>/', views.code, name='script'),
    path('code/', views.codeindex, name='script'),
    path('test/<str:type>/<str:type2>',views.server_op),
    path('console/',views.console,name='submit'),

]

