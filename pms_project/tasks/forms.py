# tasks/forms.py
from django import forms
from .models import Task
from users.models import CustomUser
from projects.models import Project

# Full form for Manager/Admin
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'status', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only employees in "assigned_to"
        self.fields['assigned_to'].queryset = CustomUser.objects.filter(role='employee')

# Form for Employee to only update status
class EmployeeTaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
