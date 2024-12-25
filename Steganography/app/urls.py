from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.api_home),
    path('', views.home, name='home'),
    path('decode/', views.decode, name='decode'),
]