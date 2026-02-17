from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class hightea(models.Model):
    sunday_date = models.DateField(unique=True)
    sponsor_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True)
    status_choices = [
        ('Booked', 'Booked'),
        ('Available', 'Available'),
        ('Null', 'Null'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Available')

    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sunday_date} - {self.sponsor_name}"