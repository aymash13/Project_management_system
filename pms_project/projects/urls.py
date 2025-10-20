from django.urls import path
from . import views

app_name = 'projects'  # important for namespacing

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/update/', views.project_update, name='project_update'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
]