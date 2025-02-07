from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(EncodeMessage)
admin.site.register(DecodeMessage)
admin.site.register(EncodeFile)
admin.site.register(DecodeFile)