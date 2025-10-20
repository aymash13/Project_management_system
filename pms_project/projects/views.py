from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Project
from users.models import CustomUser

# -------------------------------
# Form for creating/updating project
# -------------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

# -------------------------------
# List all projects (manager/admin)
# -------------------------------
@login_required
def project_list(request):
    user = request.user
    role = user.role  # can also use role.lower() if you prefer
    if role == 'Manager':
        projects = Project.objects.filter(manager=user)
    elif role == 'Admin':
        projects = Project.objects.all()
    else:
        projects = Project.objects.none()

    return render(request, 'projects/project_list.html', {'projects': projects})

# -------------------------------
# Create new project
# -------------------------------
@login_required
def project_create(request):
    role = request.user.role
    if role not in ['Manager', 'Admin']:
        messages.error(request, "You do not have permission to create a project.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user  # auto-assign manager
            project.save()
            messages.success(request, "Project created successfully.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form})

# -------------------------------
# Update existing project
# -------------------------------
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    role = request.user.role

    if request.user != project.manager and role != 'Admin':
        messages.error(request, "You do not have permission to edit this project.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {'form': form})

# -------------------------------
# View project details
# -------------------------------
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
