from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('users:login')),  # redirect home to login page
    path('users/', include('users.urls', namespace='users')),
    path('projects/', include('projects.urls')),
    path('tasks/', include('tasks.urls')),
    path('dashboard/', include('dashboard.urls')),
]