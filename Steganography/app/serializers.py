from .models import SecretMessage , DecodeMessage
from rest_framework import serializers

class SecretMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretMessage
        fields = '__all__'

class DecodeMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DecodeMessage
        fields = '__all__'