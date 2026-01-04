from django.contrib import admin
# CORREÇÃO: Importar explicitamente
from .models import Notification

# Register your models here.
admin.site.register(Notification)