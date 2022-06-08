from django.urls import path
from APPS.Login import views

urlpatterns = [
    path('', views.login, name='login'),
    path('join/', views.join, name='join'),
    path('logout/', views.logout, name='logout'),
    path('needlogin/', views.needlogin, name='needlogin'),
    path('loginok/', views.loginok, name='loginok'),
]