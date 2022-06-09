from django.urls import path
from APPS.ChatBot import views

urlpatterns = [
    path('', views.chatmain, name='chatmain'),
    path('kakaopay/', views.kakaopay, name='kakaopay'),
    path('kakaopay/approval', views.approval, name='approval')
]