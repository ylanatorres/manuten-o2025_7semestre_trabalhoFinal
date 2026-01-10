from rest_framework import routers
from django.urls import path, include
from .views import CreateEmployee

router = routers.DefaultRouter()
router.register('manage_employee', CreateEmployee, 'manage_employee')

urlpatterns = [
    path(r'', include(router.urls)),
]