from django import forms
from .models import Task
from users.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qs = CustomUser.objects.filter(role='employee')

        if user and user.role == "manager":
            qs = CustomUser.objects.filter(manager=user)

        if self.instance.pk and self.instance.project:
            qs = self.instance.project.manager.team_members.all()

        self.fields['assigned_to'].queryset = qs


class EmployeeTaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']