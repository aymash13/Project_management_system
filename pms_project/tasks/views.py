from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm, EmployeeTaskStatusForm
from projects.models import Project


@login_required
def task_list(request):
    user = request.user

    if user.role == 'manager':
        projects = Project.objects.filter(manager=user)
        tasks = Task.objects.filter(project__in=projects)
    elif user.role == 'employee':
        tasks = Task.objects.filter(assigned_to=user)
    else:
        tasks = Task.objects.none()

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    user = request.user

    if user.role != 'manager':
        messages.error(request, "You do not have permission.")
        return redirect('tasks:task_list')

    if request.method == 'POST':
        form = TaskForm(user=user, data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)

            if task.project.manager != user:
                messages.error(request, "Invalid project assignment.")
                return redirect('tasks:task_list')

            task.save()
            messages.success(request, "Task created successfully.")
            return redirect('tasks:task_list')
    else:
        form = TaskForm(user=user)

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if user.role == 'manager' and user == task.project.manager:
        form_class = TaskForm
    elif user.role == 'employee' and user == task.assigned_to:
        form_class = EmployeeTaskStatusForm
    else:
        messages.error(request, "You do not have permission.")
        return redirect('tasks:task_list')

    if request.method == 'POST':
        if form_class == TaskForm:
            form = form_class(user=user, data=request.POST, instance=task)
        else:
            form = form_class(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('tasks:task_list')
    else:
        if form_class == TaskForm:
            form = form_class(user=user, instance=task)
        else:
            form = form_class(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.user != task.project.manager:
        messages.error(request, "You do not have permission.")
        return redirect('tasks:task_list')

    task.delete()
    messages.success(request, "Task deleted successfully.")
    return redirect('tasks:task_list')