from .models import *
from rest_framework import serializers

class EncodeMessageSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(max_length=4, write_only=True)
    class Meta:
        model = EncodeMessage
        fields = ['pin','Message',  'Image',]
        

class DecodeMessageSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(max_length=4, write_only=True)
    class Meta:
        model = DecodeMessage
        fields = ['pin','Image']
        
class EncodeFileSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(max_length=4, write_only=True)
    class Meta:
        model = EncodeFile
        fields = [ 'pin','Image','File',]
        
class DecodeFileSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(max_length=4, write_only=True)
    class Meta:
        model = DecodeFile
        fields = ['Image', 'pin']  
        