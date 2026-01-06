import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

# Imports
from cinema_booking.models import Seat, Available_Slots
from .models import Cinema, CinemaDeck, MovieDurationSlot, CinemaArrangeSlot
from .serializers import (
    CinemaSerializer,
    CinemaDeckSerializer,
    MovieDurationSlotSerializer,
    CinemaArrangeSlotReadSerializer,
    CinemaArrangeSlotWriteSerializer
)

# Constantes
ACCESS_DENIED_MSG = "Access Denied"
DOES_NOT_EXIST_MSG = "Does not exist"
ACCESS_GRANTED_MSG = "Access Granted"

# --- CLASSE PAI (Resolve a Duplicação) ---
class BaseCinemaViewSet(viewsets.ModelViewSet):
    """
    Classe base que contém a lógica repetida de 'destroy' e permissões.
    Todas as outras classes vão herdar daqui.
    """
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def check_admin_employee(self):
        return self.request.user.is_admin or self.request.user.is_employee

    def destroy(self, request, *args, **kwargs):
        # Lógica genérica que serve para todos os Models
        try:
            # Busca o objeto usando o queryset da classe filha
            instance = self.get_queryset().get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        
        if self.check_admin_employee():
            instance.delete()
            return Response({"successful": ACCESS_GRANTED_MSG}, status=200)
        else:
            return Response({"error": ACCESS_DENIED_MSG}, status=401)

# --- CLASSES FILHAS (Limpas e sem repetição) ---

class CinemaViewsets(BaseCinemaViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer

    def get_queryset(self):
        return Cinema.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        if self.check_admin_employee():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status=200)
        return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            instance = Cinema.objects.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        
        if self.check_admin_employee():
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
        return Response({"error": ACCESS_DENIED_MSG}, status=401)


class CinemaDeckViewsets(BaseCinemaViewSet):
    queryset = CinemaDeck.objects.all()
    serializer_class = CinemaDeckSerializer

    def get_queryset(self):
        return CinemaDeck.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        if self.check_admin_employee():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(active=True)
            return Response(serializer.data, status=200)
        return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            instance = CinemaDeck.objects.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        
        if self.check_admin_employee():
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(updated_at=datetime.datetime.now())
                return Response(serializer.data, status=200)
        return Response({"error": ACCESS_DENIED_MSG}, status=401)


class CinemaSlotsDurationViewsets(BaseCinemaViewSet):
    queryset = MovieDurationSlot.objects.all()
    serializer_class = MovieDurationSlotSerializer

    def get_queryset(self):
        return MovieDurationSlot.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        if self.check_admin_employee():
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(active=True)
            return Response(serializer.data, status=200)
        return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            instance = MovieDurationSlot.objects.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        
        if self.check_admin_employee():
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
        return Response({"error": ACCESS_DENIED_MSG}, status=401)


class CinemaArrangeSlotViewsets(BaseCinemaViewSet):
    queryset = CinemaArrangeSlot.objects.all().order_by('created_at')
    serializer_class = CinemaArrangeSlotWriteSerializer

    def list(self, request, *args, **kwargs):
        serializer = CinemaArrangeSlotReadSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        if self.check_admin_employee():
            serializer = CinemaArrangeSlotWriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.save(active=True)
                try:
                    query = MovieDurationSlot.objects.get(id=(request.data.get('duration_slot')))
                    get_query = CinemaArrangeSlot.objects.get(id=data.id)
                    
                    fulldate = datetime.datetime(100, 1, 1, (get_query.start_time).hour, (get_query.start_time).minute,
                                                (get_query.start_time).second)
                    next_time = fulldate + datetime.timedelta(seconds=(query.duration).seconds)
                    get_query.end_time = next_time.time()
                    get_query.save()
                    
                    if data:
                        CinemaArrangeSlot.slot_updater(self=self)
                        CinemaArrangeSlot.slot_maker(self=self)
                        CinemaArrangeSlot.seat_maker(self=self)
                    
                    serializer = CinemaArrangeSlotReadSerializer(get_query)
                    return Response(serializer.data, status=200)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def update(self, request, *args, **kwargs):
        try:
            instance = CinemaArrangeSlot.objects.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        
        if self.check_admin_employee():
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=200)
        return Response({"error": ACCESS_DENIED_MSG}, status=401)