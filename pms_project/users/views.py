from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib import messages

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard:dashboard')  # redirect to dashboard after login
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'users/login.html')


# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role
            )
            messages.success(request, "Registration successful")
            return redirect('users:login')  # redirect to login after registration
    return render(request, 'users/register.html')


# Profile view
@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')  # redirect to login after logout
