from django.urls import path
from APPS.Order import views

urlpatterns = [
    path('list/', views.order_list, name='order_list'),
]