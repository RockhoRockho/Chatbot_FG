from django.urls import path
from APPS.Login import views

urlpatterns = [
    path('register/', views.register, name='register'),
]