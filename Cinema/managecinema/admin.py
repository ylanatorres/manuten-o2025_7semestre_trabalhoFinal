from django.contrib import admin
# CORREÇÃO: Importar explicitamente apenas os modelos usados
from .models import Cinema, CinemaDeck, CinemaArrangeSlot, MovieDurationSlot

# Register your models here.
admin.site.register(Cinema)
admin.site.register(CinemaDeck)
admin.site.register(CinemaArrangeSlot)
admin.site.register(MovieDurationSlot)