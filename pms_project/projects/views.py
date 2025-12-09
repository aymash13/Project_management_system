from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Project


# -------------------------------
# Form
# -------------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }


# -------------------------------
# List Projects
# -------------------------------
@login_required
def project_list(request):
    user = request.user
    
    if user.role == 'manager':
        projects = Project.objects.filter(manager=user)
    else:
        projects = Project.objects.none()  # employees cannot view projects list

    return render(request, 'projects/project_list.html', {'projects': projects})


# -------------------------------
# Create Project
# -------------------------------
@login_required
def project_create(request):
    user = request.user

    if user.role != 'manager':
        messages.error(request, "Only managers can create projects.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = user
            project.save()
            messages.success(request, "Project created successfully.")
            return redirect('projects:project_list')
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form})


# -------------------------------
# Update Project
# -------------------------------
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user

    if project.manager != user:
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
# View Details
# -------------------------------
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.role == "employee" and request.user not in project.manager.team_members.all():
        messages.error(request, "You do not have access to this project.")
        return redirect("projects:project_list")

    return render(request, 'projects/project_detail.html', {'project': project})