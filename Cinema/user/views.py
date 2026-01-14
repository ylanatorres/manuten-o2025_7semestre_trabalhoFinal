from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_anonymous:
            return User.objects.none()

        if user.is_superuser or getattr(user, 'is_admin', False):
            return User.objects.all()
            
        return User.objects.filter(id=user.id)

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User  
from django.contrib import messages

#tela de Cadastro
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "As senhas não conferem!")
            return redirect('register')

        #cria o usuário
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)  
            return redirect('home') 
        except Exception as e:
            messages.error(request, f"Erro ao criar usuário: {e}")
            return redirect('register')

    return render(request, 'register.html')

#tela de Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    
    return render(request, 'login.html')

#logout 
def logout_view(request):
    logout(request)
    return redirect('login')