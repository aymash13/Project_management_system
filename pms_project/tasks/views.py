# tasks/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm, EmployeeTaskStatusForm
from projects.models import Project

# List tasks
@login_required
def task_list(request):
    user = request.user
    if user.role.lower() == 'admin':
        tasks = Task.objects.all()
    elif user.role.lower() == 'manager':
        projects = Project.objects.filter(manager=user)
        tasks = Task.objects.filter(project__in=projects)
    elif user.role.lower() == 'employee':
        tasks = Task.objects.filter(assigned_to=user)
    else:
        tasks = Task.objects.none()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Manager view for their project tasks
@login_required
def manager_tasks(request):
    if request.user.role.lower() != 'manager':
        messages.error(request, "You do not have permission")
        return redirect('dashboard:dashboard')
    projects = Project.objects.filter(manager=request.user)
    tasks = Task.objects.filter(project__in=projects)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Create task
@login_required
def task_create(request):
    if request.user.role.lower() not in ['manager', 'admin']:
        messages.error(request, "You do not have permission")
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully")
            return redirect('tasks:task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form})

# Update task
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)

    # Determine which form to use
    if request.user.role.lower() == 'admin' or request.user == task.project.manager:
        form_class = TaskForm
    elif request.user.role.lower() == 'employee' and request.user == task.assigned_to:
        form_class = EmployeeTaskStatusForm
    else:
        messages.error(request, "You do not have permission to edit this task.")
        return redirect('tasks:task_list')

    if request.method == 'POST':
        form = form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('tasks:task_list')
    else:
        form = form_class(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form})

# Task detail
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

# Delete task
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user.role.lower() != 'admin' and request.user != task.project.manager:
        messages.error(request, "You do not have permission to delete this task.")
        return redirect('tasks:task_list')
    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('tasks:task_list')
