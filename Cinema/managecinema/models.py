import datetime
from django.db import models
from djmoney.models.fields import MoneyField

# Imports dos modelos externos
from cinema_booking.models import AvailableSlots, SeatManager, Seat
class Cinema(models.Model):
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=200, unique=True)
    release_date = models.DateField(auto_now=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    all_review = models.ManyToManyField('cinema_feedback.Review', blank=True)

    def __str__(self):
        return "{}-{}".format(self.movie_name, self.release_date)


class CinemaDeck(models.Model):
    id = models.AutoField(primary_key=True)
    deck_name = models.CharField(max_length=200, unique=True)
    price = MoneyField(default=0, default_currency='INR', max_digits=11)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}{}".format(self.deck_name, self.price)


class MovieDurationSlot(models.Model):
    id = models.AutoField(primary_key=True)
    duration = models.DurationField(unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.duration, self.active)


class CinemaArrangeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    cinema = models.ForeignKey("managecinema.Cinema", on_delete=models.CASCADE)
    start_time = models.TimeField(unique=True)
    duration_slot = models.ForeignKey("managecinema.MovieDurationSlot", on_delete=models.CASCADE)
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.cinema, self.start_time)

    # --- CORREÇÃO: Redução de Complexidade Cognitiva ---
    def slot_maker(self):
        # Busca slots existentes
        slots = CinemaArrangeSlot.objects.all()
        today = datetime.date.today()
        
        for slot in slots:
            # Cria para hoje (se não existir)
            AvailableSlots.objects.get_or_create(
                slot=slot, 
                date=today, 
                defaults={'active': True}
            )
            
            # Cria para os próximos 2 dias
            current_date = today
            for _ in range(2):
                current_date += datetime.timedelta(days=1)
                AvailableSlots.objects.get_or_create(
                    slot=slot, 
                    date=current_date, 
                    defaults={'active': True}
                )

    # --- CORREÇÃO: Redução Drástica de Loops Aninhados e ifs ---
    def seat_maker(self):
        decks = CinemaDeck.objects.filter(active=True)
        managers = SeatManager.objects.all()
        active_slots = AvailableSlots.objects.filter(active=True)

        for deck in decks:
            for manager in managers:
                for slot in active_slots:
                    for name_idx in range(0, 2):
                        # get_or_create substitui toda aquela lógica de "if not exists: create else: pass"
                        # Isso resolve o erro de complexidade do SonarCloud
                        Seat.objects.get_or_create(
                            name=name_idx,
                            deck=deck,
                            date=slot.date,
                            seat=manager,
                            available_slot=slot
                        )

    def slot_updater(self):
        # Lógica otimizada: Filtra apenas os slots antigos e desativa
        # Isso evita loops desnecessários e try/except vazios
        yesterday_limit = datetime.datetime.now() - datetime.timedelta(days=1)
        
        # Considerando que 'date' em Available_Slots é um DateField
        expired_slots = AvailableSlots.objects.filter(
            date__lt=yesterday_limit.date(), 
            active=True
        )
        
        # Atualização em massa é mais eficiente
        expired_slots.update(active=False)