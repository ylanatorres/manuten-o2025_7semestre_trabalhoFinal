from rest_framework import routers
from django.urls import path, include

# --- CORREÇÃO DO SONAR: Importar explicitamente as Viewsets usadas ---
from .views import (
    CinemaViewsets, 
    CinemaDeckViewsets, 
    CinemaSlotsDurationViewsets, 
    CinemaArrangeSlotViewsets
)

router = routers.DefaultRouter()
router.register('cinema', CinemaViewsets, 'cinema')
router.register('cinema_deck', CinemaDeckViewsets, 'cinema_deck')
router.register('cinema_slots_duration', CinemaSlotsDurationViewsets, 'cinema_slots_duration')
router.register('cinema_arrange_slot', CinemaArrangeSlotViewsets, 'cinema_arrange_slot')

urlpatterns = [
    path(r'', include(router.urls)),
]