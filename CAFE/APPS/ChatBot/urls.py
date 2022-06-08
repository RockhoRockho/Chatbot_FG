from django.urls import path
from APPS.ChatBot import views

urlpatterns = [
    path('', views.chatmain, name='chatmain'),
]