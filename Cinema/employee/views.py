from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound

from user.models import User
from .models import Employee
from .serializers import EmployeeSerializer

ACCESS_DENIED_MSG = "Access Denied"
DOES_NOT_EXIST_MSG = "Does not exist"

class CreateEmployee(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        if request.user.is_admin or self.request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                try:
                    user_query = User.objects.get(id=request.data.get('user'))
                    user_query.is_employee = True
                    user_query.save()
                    
                    serializer.save(first_Name=user_query.first_name, last_Name=user_query.last_name)
                    return Response(serializer.data, status=200)
                except User.DoesNotExist:
                    return Response({"ERROR": DOES_NOT_EXIST_MSG}, status=400)
        else:
            return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_admin or self.request.user.is_superuser:
            try:
                queryset = Employee.objects.get(id=self.kwargs["id"])
                serializer = EmployeeSerializer(queryset)
                return Response(serializer.data, status=200)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": DOES_NOT_EXIST_MSG}, status=400)
        else:
            return Response({"NO_ACCESS": ACCESS_DENIED_MSG}, status=401)

    def perform_update(self, serializer):
        if self.request.user.is_admin or self.request.user.is_superuser:
            serializer.save()
        else:
            raise PermissionDenied(ACCESS_DENIED_MSG)

    def perform_destroy(self, instance):
        if self.request.user.is_admin or self.request.user.is_superuser:
            try:
                user_query = instance.user
                if user_query:
                    user_query.is_employee = False
                    user_query.save()
                
                instance.delete()
            except ObjectDoesNotExist:
                raise NotFound(DOES_NOT_EXIST_MSG)
        else:
            raise PermissionDenied(ACCESS_DENIED_MSG)