from django.contrib import admin
# CORREÇÃO: Importar explicitamente
from .models import Employee

# Register your models here.
admin.site.register(Employee)