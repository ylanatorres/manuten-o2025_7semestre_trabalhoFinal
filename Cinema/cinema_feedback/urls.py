from django.urls import path
from .views import ReviewViewsets

urlpatterns = [
    path('', ReviewViewsets.as_view()),
]