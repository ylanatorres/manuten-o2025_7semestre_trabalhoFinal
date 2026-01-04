from django.contrib import admin
# --- CORREÇÃO: Importar apenas Review ---
from .models import Review

# Register your models here.
admin.site.register(Review)