from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.urls import path, include

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
    path('home/', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('booking/<int:movie_id>/<str:session_time>/', views.seat_selection, name='seat_selection'),
    path('booking/finish/', views.booking_finish, name='booking_finish'),
]