from rest_framework import routers
from django.urls import path, include
# CORREÇÃO: Importar explicitamente as Viewsets
from .views import BookSeatsViewsets, SeatManagerViewsets, AvailableSlotsViewsets

router = routers.DefaultRouter()
router.register('book_seat', BookSeatsViewsets, 'book_seat')
router.register('seat_manager', SeatManagerViewsets, 'seat_manager')
# Adicionei este pois geralmente está junto
router.register('available_slots', AvailableSlotsViewsets, 'available_slots') 

urlpatterns = [
    path(r'', include(router.urls)),
]