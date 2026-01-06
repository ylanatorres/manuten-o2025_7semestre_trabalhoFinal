from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # CORREÇÃO: Se o usuário for anônimo (Swagger), retorna lista vazia para não dar erro
        if user.is_anonymous:
            return User.objects.none()

        # Agora é seguro verificar is_admin
        if user.is_superuser or getattr(user, 'is_admin', False):
            return User.objects.all()
            
        return User.objects.filter(id=user.id)