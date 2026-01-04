from rest_framework import routers
from django.urls import path, include
# CORREÇÃO: Importar explicitamente as Views usadas nas URLs
from .views import NotificationListView, UnreadNotificationCount

urlpatterns = [
    path('notification/', NotificationListView.as_view()),
    path('unread_notification_count/', UnreadNotificationCount.as_view(), name='unread_notification_count'),
]