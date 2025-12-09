from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    email = models.EmailField(unique=True)

    manager = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='team_members',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.username} ({self.role})"