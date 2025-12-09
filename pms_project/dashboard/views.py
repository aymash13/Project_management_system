from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from projects.models import Project
from tasks.models import Task


@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.role == 'manager':
        projects = Project.objects.filter(manager=user)
        
        context.update({
            'total_projects': projects.count(),
            'total_tasks': Task.objects.filter(project__in=projects).count(),
            'tasks_by_status': Task.objects.filter(project__in=projects)
                                      .values('status')
                                      .annotate(count=Count('id')),
        })

    elif user.role == 'employee':
        employee_tasks = Task.objects.filter(assigned_to=user)

        context.update({
            'total_tasks': employee_tasks.count(),
            'tasks_by_status': employee_tasks
                                .values('status')
                                .annotate(count=Count('id')),
        })

    else:
        context.update({
            'message': "Access dashboards via Django admin panel."
        })

    return render(request, 'dashboard/dashboard.html', context)