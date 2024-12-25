from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Users(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]

    username = models.CharField(max_length=255, 
                                unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, 
                            default='User')
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255, 
                             unique=True)
    description = models.TextField(blank=True, 
                                   null=True)
    status = models.CharField(max_length=11, 
                              choices=STATUS_CHOICES, 
                              default='Pending')
    priority = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), 
                                                            MaxValueValidator(5)])
    created_by = models.ForeignKey('Users', 
                                   on_delete=models.CASCADE, 
                                   related_name='tasks_created')
    assigned_to = models.ForeignKey('Users', 
                                    on_delete=models.SET_NULL, 
                                    null=True, 
                                    blank=True, 
                                    related_name='tasks_assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class TaskHistory(models.Model):
    task = models.ForeignKey('Task', 
                             on_delete=models.CASCADE, 
                             related_name='history') 
    changed_by = models.ForeignKey('Users', 
                                   on_delete=models.CASCADE, 
                                   related_name='changes_made')
    change_details = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)