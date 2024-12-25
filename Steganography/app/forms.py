from django import forms
from .models import SecretMessage , DecodeMessage

class SecretMessageForm(forms.ModelForm):
    class Meta:
        model = SecretMessage
        fields = ['Message','Image']
        
class DecodeMessageForm(forms.ModelForm):
    class Meta:
        model = DecodeMessage
        fields = ['Image']
        