from django.urls import path
# --- CORREÇÃO: Importar apenas a Viewset usada ---
from .views import ReviewViewsets

urlpatterns = [
    path('', ReviewViewsets.as_view()),
]