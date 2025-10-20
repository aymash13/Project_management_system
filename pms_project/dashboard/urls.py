from django.urls import path
from . import views

app_name = 'dashboard'  # ← THIS IS REQUIRED

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # /dashboard/
]
