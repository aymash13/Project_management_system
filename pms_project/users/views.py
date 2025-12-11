from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import RegisterForm, ProfileUpdateForm


# Login View
def login_view(request):
    next_page = request.GET.get("next", "dashboard:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_page)
        else:
            messages.error(request, "Invalid Credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')  # already logged in
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Registration successful")
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {'user': request.user})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("users:login")


@login_required
def profile_update(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = ProfileUpdateForm(instance=user, user=user)

    return render(request, "users/profile_update.html", {'form': form})