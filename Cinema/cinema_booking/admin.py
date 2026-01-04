from django.contrib import admin
# Substituímos o '*' pelos nomes específicos das classes
from .models import AvailableSlots, Seat, seat_manager, BookSeat

# Register your models here.
admin.site.register(AvailableSlots) 
admin.site.register(Seat)
admin.site.register(seat_manager)
admin.site.register(BookSeat)