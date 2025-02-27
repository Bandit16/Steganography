from django.urls import path
from . import views

urlpatterns = [
    path('api/encode_file/', views.api_encode_file),
    path('api/encode_message/', views.api_encode_message),
    path('api/decode_file/', views.api_decode_file),
    path('api/decode_message/', views.api_decode_message),
    path('encode_file/', views.encode_file, name='encode_file'),
    path('encode_message/', views.encode_message, name='encode_message'),
    path('decode_file/', views.decode_file, name='decode_file'),
    path('decode_message/', views.decode_message, name='decode_message'),
    path('about/', views.about, name='about'),
    path('document/',views.document, name='document'),
    path('', views.home, name='home'),
]