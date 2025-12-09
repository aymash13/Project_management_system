from django.db import models
from users.models import CustomUser

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="projects",
        limit_choices_to={'role': 'manager'}
    )

    def __str__(self):
        return self.name