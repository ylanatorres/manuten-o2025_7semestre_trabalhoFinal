from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# Seus Imports
from cinema_notification.models import Notification
from managecinema.models import CinemaArrangeSlot, CinemaDeck, Cinema
from .models import AvailableSlots, Seat, BookSeat, SeatManager
from .serializers import (
    AvailableSlotsReadSerializer, 
    SeatSerializer, 
    BookSeatSerializer, 
    SeatManagerSerializer
)

# Constantes
ACCESS_DENIED_MSG = "Access Denied"
DOES_NOT_EXIST_MSG = "Does not exist"

# --- MUDANÇA PRINCIPAL 1: Herdar de ReadOnlyModelViewSet ---
# Antes era generics.ListAPIView (que quebra o Router). 
# Agora é ViewSet, mas ReadOnly (apenas leitura/listagem), que é o que o ListAPIView fazia.
class AvailableSlotsViewsets(viewsets.ReadOnlyModelViewSet):
    queryset = AvailableSlots.objects.all().order_by('-date')
    serializer_class = AvailableSlotsReadSerializer
    filter_backends = [SearchFilter]
    search_fields = ['date']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


# --- MUDANÇA PRINCIPAL 2: Transformar SeatsList em ViewSet ---
# Se você tiver uma rota para isso no router, precisa ser ViewSet também.
class SeatsViewsets(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.all().order_by('-date')
    serializer_class = SeatSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'deck__deck_name', 'date']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Sua lógica personalizada de atualização
        CinemaArrangeSlot.slot_updater(self=self)
        CinemaArrangeSlot.slot_maker(self=self)
        CinemaArrangeSlot.seat_maker(self=self)
        Seat.seat_updater(self=self)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class BookSeatsViewsets(viewsets.ModelViewSet):
    queryset = BookSeat.objects.all().order_by('-created_at')
    serializer_class = BookSeatSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return BookSeat.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_admin or request.user.is_employee or request.user.is_customer:
                try:
                    seat_query = Seat.objects.get(id=request.data.get('seat'))
                    deck_query = CinemaDeck.objects.get(id=seat_query.deck.id)
                    available_slot_query = AvailableSlots.objects.get(id=seat_query.available_slot.id) 
                    arrange_slot_query = CinemaArrangeSlot.objects.get(id=available_slot_query.slot.id)
                    cinema_query = Cinema.objects.get(id=arrange_slot_query.cinema.id)
                    
                    booked_seat = serializer.save(user=request.user, booking_price=deck_query.price)
                    
                    Seat.seat_book(self=self, seat=request.data.get('seat'), user=request.user)
                    
                    Notification.objects.create(
                        seat=booked_seat, 
                        user=request.user,
                        text="Hello {}, you have book movie {}, on date {}.".format(
                            request.user,
                            cinema_query.movie_name,
                            available_slot_query.date
                        )
                    )
                    
                    BookSeat.send_mail(
                        user=request.user, 
                        movie=cinema_query.movie_name,
                        date=available_slot_query.date, 
                        email=request.user.email, 
                        self=self
                    )
                    return Response(serializer.data, status=200)
                
                except ObjectDoesNotExist:
                     return Response({"ERROR": DOES_NOT_EXIST_MSG}, status=400)
            else:
                return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_employee or request.user.is_customer:
            try:
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=200)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        else:
            return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def perform_update(self, serializer):
        if self.request.user.is_admin or self.request.user.is_employee:
            serializer.save(updated_at=datetime.now())
        else:
            raise PermissionDenied(ACCESS_DENIED_MSG)

    def perform_destroy(self, instance):
        if self.request.user.is_admin or self.request.user.is_employee:
            instance.delete()
        else:
            raise PermissionDenied(ACCESS_DENIED_MSG)


class SeatManagerViewsets(viewsets.ModelViewSet):
    queryset = SeatManager.objects.all().order_by('-created_at')
    serializer_class = SeatManagerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return SeatManager.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_admin or self.request.user.is_employee:
            serializer.save()
        else:
            raise PermissionDenied(ACCESS_DENIED_MSG)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_admin or request.user.is_employee:
            try:
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data, status=200)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        else:
            return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def update(self, request, *args, **kwargs):
        if not (request.user.is_admin or request.user.is_employee):
            return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)
            
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=True):
                serializer.save(updated_at=datetime.now())
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)

    def perform_destroy(self, instance):
        if self.request.user.is_admin or self.request.user.is_superuser:
            instance.delete()
        else:
            raise PermissionDenied(ACCESS_DENIED_MSG)