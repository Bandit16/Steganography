from django import forms
from .models import SecretMessage , DecodeMessage

class SecretMessageForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)

    class Meta:
        model = SecretMessage
        fields = ['Message', 'pin', 'Image','File']
        
class DecodeMessageForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput)
    class Meta:
        model = DecodeMessage
        fields = ['Image' , 'pin' ,]
        