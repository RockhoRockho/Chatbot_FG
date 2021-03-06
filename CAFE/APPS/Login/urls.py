from django.urls import path
from APPS.Login import views

urlpatterns = [
    path('', views.login, name='login'),
    path('join/', views.join, name='join'),
    path('logout/', views.logout, name='logout'),
    path('needlogin/', views.needlogin, name='needlogin'),
    path('loginok/', views.loginok, name='loginok'),
    path('joinok/', views.joinok, name='joinok'),
    path('needlogin2/', views.needlogin2, name='needlogin2'),
]