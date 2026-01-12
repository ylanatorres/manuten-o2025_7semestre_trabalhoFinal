from django.contrib import admin
from .models import AvailableSlots, Seat, SeatManager, BookSeat
# Register your models here.
admin.site.register(AvailableSlots) 
admin.site.register(Seat)
admin.site.register(SeatManager)
admin.site.register(BookSeat)