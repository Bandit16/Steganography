from django.urls import path
from . import views

urlpatterns = [
    path('api/encode/', views.api_home),
    path('api/decode/', views.api_decode),
    path('', views.home, name='home'),
    path('decode/', views.decode, name='decode'),
]