from django import forms
from .models import *

class EncodeMessageForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'value': '0000',}))

    class Meta:
        model = EncodeMessage
        fields = ['Message', 'pin', 'Image',]
        
class DecodeMessageForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'value': '0000'}))
    class Meta:
        model = DecodeMessage
        fields = ['Image' , 'pin' ,]
        
class EncodeFileForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'value': '0000'}))
    class Meta:
        model = EncodeFile
        fields = ['pin', 'Image','File',]


class DecodeFileForm(forms.ModelForm):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={'value': '0000'}))
    class Meta:
        model = DecodeFile
        fields = ['Image' , 'pin' ,]