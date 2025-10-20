from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # ← import Count
from projects.models import Project
from tasks.models import Task
from users.models import CustomUser

@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role.lower() == 'admin':
        total_projects = Project.objects.count()
        total_tasks = Task.objects.count()
        total_users = CustomUser.objects.count()
        tasks_by_status = Task.objects.values('status').order_by('status').annotate(count=Count('id'))
        context.update({
            'total_projects': total_projects,
            'total_tasks': total_tasks,
            'total_users': total_users,
            'tasks_by_status': tasks_by_status,
        })
    elif user.role.lower() == 'manager':
        projects = Project.objects.filter(manager=user)
        total_projects = projects.count()
        total_tasks = Task.objects.filter(project__in=projects).count()
        tasks_by_status = Task.objects.filter(project__in=projects).values('status').annotate(count=Count('id'))
        context.update({
            'total_projects': total_projects,
            'total_tasks': total_tasks,
            'tasks_by_status': tasks_by_status,
        })
    elif user.role.lower() == 'employee':
        tasks = Task.objects.filter(assigned_to=user)
        total_tasks = tasks.count()
        tasks_by_status = tasks.values('status').annotate(count=Count('id'))
        context.update({
            'total_tasks': total_tasks,
            'tasks_by_status': tasks_by_status,
        })

    return render(request, 'dashboard/dashboard.html', context)
