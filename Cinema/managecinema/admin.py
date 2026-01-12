from django.contrib import admin
from .models import Cinema, CinemaDeck, CinemaArrangeSlot, MovieDurationSlot

admin.site.register(Cinema)
admin.site.register(CinemaDeck)
admin.site.register(CinemaArrangeSlot)
admin.site.register(MovieDurationSlot)