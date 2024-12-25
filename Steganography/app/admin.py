from django.contrib import admin
from .models import SecretMessage ,DecodeMessage

# Register your models here.
admin.site.register(SecretMessage)
admin.site.register(DecodeMessage)